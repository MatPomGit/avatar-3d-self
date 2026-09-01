import json
from pathlib import Path

from avatar_studio.adapters.base import CommandResult
from avatar_studio.adapters.blender import BlenderAdapter, _REPORT_MARKER
from avatar_studio.adapters.colmap import ColmapAdapter
from avatar_studio.adapters.ffmpeg import FFmpegAdapter
from avatar_studio.adapters.piper import PiperAdapter


def test_blender_scene_report_parser():
    payload = {"meshes": 2, "vertices": 1234, "shape_keys": 52, "fps": 60.0}
    result = CommandResult(
        ("blender",),
        0,
        "Blender 4.x\n" + _REPORT_MARKER + json.dumps(payload) + "\n",
        "",
    )
    assert BlenderAdapter._parse_report(result) == payload


def test_colmap_model_analyzer_parser():
    text = """
Cameras: 1
Images: 36
Registered images: 34
Points: 123456
Observations: 654321
Mean track length: 5.30
Mean observations per image: 19244.74
Mean reprojection error: 0.47px
"""
    metrics = ColmapAdapter.parse_model_analyzer(text)
    assert metrics["cameras"] == 1
    assert metrics["images"] == 36
    assert metrics["registered_images"] == 34
    assert metrics["points3d"] == 123456
    assert metrics["mean_reprojection_error_px"] == 0.47
    assert metrics["registration_ratio"] == 34 / 36


def test_ffmpeg_audio_metadata_parser():
    text = """
Duration: 00:00:12.50, start: 0.000000, bitrate: 705 kb/s
  Stream #0:0: Audio: pcm_s16le, 22050 Hz, mono, s16, 352 kb/s
"""
    report = FFmpegAdapter.parse_audio_metadata(text)
    assert report["duration_s"] == 12.5
    assert report["codec"] == "pcm_s16le"
    assert report["sample_rate_hz"] == 22050
    assert report["channels"] == 1
    assert report["bit_rate_kbps"] == 352


def test_piper_reads_adjacent_model_config(tmp_path):
    model = tmp_path / "pl_PL-test-medium.onnx"
    model.write_bytes(b"model")
    config = Path(str(model) + ".json")
    config.write_text(json.dumps({"audio": {"sample_rate": 22050}}), encoding="utf-8")
    assert PiperAdapter.find_model_config(model) == config
    assert PiperAdapter._sample_rate(PiperAdapter.read_model_config(config)) == 22050


def test_piper_synthesis_records_provenance(tmp_path, monkeypatch):
    model = tmp_path / "voice.onnx"
    model.write_bytes(b"voice model")
    config = Path(str(model) + ".json")
    config.write_text(json.dumps({"audio": {"sample_rate": 22050}}), encoding="utf-8")
    output = tmp_path / "speech.wav"
    executable = tmp_path / "piper"
    executable.write_text("fake", encoding="utf-8")
    adapter = PiperAdapter(executable=executable)

    def fake_run(args, **kwargs):
        assert kwargs["input_text"] == "Ala ma kota.\n"
        output.write_bytes(b"RIFF fake wav")
        return CommandResult((str(executable), *map(str, args)), 0, "", "")

    monkeypatch.setattr(adapter, "run", fake_run)
    report = adapter.synthesize("Ala ma kota.", model, output, length_scale=1.05)
    assert report["sample_rate_hz"] == 22050
    assert report["output_sha256"]
    assert report["model_sha256"]
    assert report["text_characters"] == len("Ala ma kota.")
    assert report["parameters"]["length_scale"] == 1.05


def test_piper_http_alignment_becomes_start_end_timing():
    payload = {
        "voice": {"name": "pl_PL-test-medium", "language": "pl", "num_speakers": 1},
        "last": {
            "text": "ma",
            "synthesize_seconds": 0.08,
            "phonemes": ["m", "a"],
            "alignments": [
                {"phoneme": "m", "seconds": 0.06},
                {"phoneme": "a", "seconds": 0.14},
            ],
        },
    }
    report = PiperAdapter.normalize_http_info(payload, source_url="http://127.0.0.1:5000/info")
    assert report["last_available"] is True
    assert report["duration_s"] == 0.2
    assert report["phonemes"][0] == {
        "symbol": "m",
        "start_s": 0.0,
        "end_s": 0.06,
        "duration_s": 0.06,
    }
    assert report["phonemes"][1]["start_s"] == 0.06
    assert report["phonemes"][1]["end_s"] == 0.2
    assert "text" not in report


def test_ffmpeg_normalization_builds_pcm_wav_contract(tmp_path, monkeypatch):
    source = tmp_path / "source.wav"
    source.write_bytes(b"source")
    output = tmp_path / "normalized.wav"
    executable = tmp_path / "ffmpeg"
    executable.write_text("fake", encoding="utf-8")
    adapter = FFmpegAdapter(executable=executable)

    def fake_run(args, **kwargs):
        output.write_bytes(b"normalized")
        return CommandResult((str(executable), *map(str, args)), 0, "", "")

    monkeypatch.setattr(adapter, "run", fake_run)
    report = adapter.normalize_wav(source, output, sample_rate_hz=22050, channels=1)
    assert report["codec"] == "pcm_s16le"
    assert report["sample_rate_hz"] == 22050
    assert report["channels"] == 1
    assert report["output_sha256"]
