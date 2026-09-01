"""Canonical stage definitions used by Avatar Studio."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StageDefinition:
    """Describe one production stage and its dependency contract."""

    stage_id: str
    order: int
    title: str
    document: str
    summary: str
    dependencies: tuple[str, ...] = ()
    expected_outputs: tuple[str, ...] = ()


STAGES: tuple[StageDefinition, ...] = (
    StageDefinition("01-reference-acquisition", 1, "Reference acquisition", "pipeline/01-reference-acquisition/", "Collect calibrated references, measurements and manifests.", expected_outputs=("capture_manifest.json",)),
    StageDefinition("02-photogrammetry", 2, "Photogrammetry", "pipeline/02-photogrammetry/", "Register images and validate camera coverage.", ("01-reference-acquisition",), ("sparse reconstruction",)),
    StageDefinition("03-reconstruction", 3, "Reconstruction", "pipeline/03-reconstruction/", "Generate dense geometry at known scale.", ("02-photogrammetry",), ("avatar_scan_vNNN.ply",)),
    StageDefinition("04-mesh-cleanup", 4, "Mesh cleanup", "pipeline/04-mesh-cleanup/", "Clean high-poly geometry without changing identity.", ("03-reconstruction",), ("avatar_body_clean_vNNN.blend",)),
    StageDefinition("05-retopology", 5, "Retopology", "pipeline/05-retopology/", "Create deformation-ready topology and freeze it.", ("04-mesh-cleanup",), ("avatar_body_retopo_vNNN.blend",)),
    StageDefinition("06-uv", 6, "UV", "pipeline/06-uv/", "Create stable UV layouts and texel-density report.", ("05-retopology",), ("approved UV layout",)),
    StageDefinition("07-pbr-materials", 7, "PBR materials", "pipeline/07-pbr-materials/", "Create physically plausible skin and material maps.", ("06-uv",), ("PBR texture set",)),
    StageDefinition("08-eyes", 8, "Eyes", "pipeline/08-eyes/", "Build physically plausible eyes and eyelid interaction.", ("05-retopology",), ("eye assets",)),
    StageDefinition("09-hair-and-facial-hair", 9, "Hair and facial hair", "pipeline/09-hair-and-facial-hair/", "Build groom/cards and facial hair.", ("05-retopology",), ("groom assets",)),
    StageDefinition("10-clothing", 10, "Clothing", "pipeline/10-clothing/", "Build editable garments with their own materials.", ("05-retopology",), ("clothing assets",)),
    StageDefinition("11-glasses", 11, "Glasses", "pipeline/11-glasses/", "Reconstruct measured frames and lenses.", ("05-retopology",), ("glasses asset",)),
    StageDefinition("12-body-rig", 12, "Body rig", "pipeline/12-body-rig/", "Create canonical skeleton and controls.", ("05-retopology",), ("body rig",)),
    StageDefinition("13-hand-rig", 13, "Hand rig", "pipeline/13-hand-rig/", "Rig every finger and validate functional grasps.", ("12-body-rig",), ("hand rig",)),
    StageDefinition("14-facial-rig", 14, "Facial rig", "pipeline/14-facial-rig/", "Create jaw, eyes and ARKit/FACS-compatible facial control.", ("08-eyes", "12-body-rig"), ("facial rig", "ARKit mapping")),
    StageDefinition("15-secondary-motion", 15, "Secondary motion", "pipeline/15-secondary-motion/", "Add controlled hair, garment and anatomy-dependent dynamics.", ("09-hair-and-facial-hair", "10-clothing", "12-body-rig", "14-facial-rig"), ("secondary rigs",)),
    StageDefinition("16-skinning", 16, "Skinning", "pipeline/16-skinning/", "Approve body, face and garment deformation.", ("10-clothing", "12-body-rig", "13-hand-rig", "14-facial-rig"), ("approved skin weights", "deformation report")),
    StageDefinition("17-animation", 17, "Animation", "pipeline/17-animation/", "Create layered motion, gaze, blink, gesture and idle behaviour.", ("16-skinning",), ("validation clips",)),
    StageDefinition("18-lip-sync", 18, "Lip-sync", "pipeline/18-lip-sync/", "Generate phoneme-driven viseme and jaw curves with coarticulation.", ("14-facial-rig", "16-skinning"), ("viseme mapping",)),
    StageDefinition("19-piper-integration", 19, "Piper integration", "pipeline/19-piper-integration/", "Connect custom TTS audio to phoneme timing and facial curves.", ("18-lip-sync",), ("speech validation clip",)),
    StageDefinition("20-export", 20, "Export", "pipeline/20-export/", "Create target-specific interchange packages and reports.", ("07-pbr-materials", "08-eyes", "09-hair-and-facial-hair", "10-clothing", "11-glasses", "15-secondary-motion", "16-skinning", "17-animation", "19-piper-integration"), ("runtime package", "conversion report")),
    StageDefinition("21-runtime-validation", 21, "Runtime validation", "pipeline/21-runtime-validation/", "Run acceptance tests and measure target performance.", ("20-export",), ("runtime validation report",)),
)


STAGE_BY_ID = {stage.stage_id: stage for stage in STAGES}


def get_stage(stage_id: str) -> StageDefinition:
    """Return a stage definition or raise a clear KeyError."""

    try:
        return STAGE_BY_ID[stage_id]
    except KeyError as exc:
        raise KeyError(f"Unknown pipeline stage: {stage_id}") from exc
