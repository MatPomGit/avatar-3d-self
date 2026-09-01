# Capture manifest

Manifest opisuje sesję bez konieczności publikowania zdjęć.

```json
{
  "schema_version": 1,
  "session_id": "face-neutral-001",
  "capture_type": "photogrammetry",
  "device": "camera model",
  "lens": "main-1x",
  "resolution": [6000, 4000],
  "lighting": "diffuse-fixed",
  "pose": "neutral",
  "image_count": 96,
  "known_scale_mm": 1800.0,
  "notes": [],
  "privacy": {"public": false}
}
```

## Windows

Przechowuj manifest obok prywatnej sesji, np. `D:\Avatar3D\projects\self-avatar\capture\face\capture_manifest.json`.

## Linux

Przechowuj go analogicznie w `~/Avatar3D/projects/self-avatar/capture/face/capture_manifest.json`.

Nie zapisuj GPS, adresu ani danych kontaktowych, jeśli nie są technicznie konieczne. Avatar Studio powinno walidować schema version i brak wymaganych pól przed uruchomieniem rekonstrukcji.
