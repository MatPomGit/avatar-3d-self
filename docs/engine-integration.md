# Engine integration

The first runtime target has not yet been selected. This document defines a
validation contract rather than claiming a completed multi-engine integration.
Use a target-specific export workflow only after M3 in the roadmap has passed.

## Common import package

Every import candidate requires:

- the asset and its conversion report;
- documented units, up axis and source application;
- PBR textures with unambiguous paths or embedding policy;
- an explicit skeleton, skin-weight and morph-target mapping;
- an animation and viseme mapping when speech is included;
- a short validation clip and known limitations.

Import the package in a fresh target project before making target-specific
optimisations. Verify that the loss report matches what the application imports.

## Unreal Engine

FBX is the preferred starting interchange path when it preserves the required
skeleton and morph targets. Confirm centimetre units, skeletal mesh assignment,
material slots, LOD strategy, eye aim, facial controls and audio-driven curves
in the actual Unreal version. MetaHuman assets require separate workstation
integration and must not be assumed compatible from a filename or topology.

**Acceptance check:** a sequenced clip demonstrates idle motion, blink, gaze,
speech, facial expression and a hand gesture without deformation errors.

## Unity

Choose FBX or GLB only after checking the imported rig and blendshape names in
the target Unity and render-pipeline version. Rebuild PBR materials for URP or
HDRP as necessary; texture and shader equivalence is not guaranteed by format
conversion.

**Acceptance check:** a scene renders the avatar with correct scale, materials,
facial controls and animation at the agreed target frame time.

## Web viewer

The public viewer is static and uses a web-oriented GLB or glTF package. It is
not a substitute for the editable master or a private avatar runtime. Keep
source photos, voice audio, API keys and unapproved personal assets out of its
bundle.

**Acceptance check:** a production build loads the approved public asset,
handles missing optional assets safely and meets the browser performance budget.

## Speech integration

Use the chain text to Piper audio to phoneme or viseme timing to target
animation. Layer visemes with jaw, eye, blink, head and emotion controls. Do
not drive facial animation only from audio amplitude. Store the mapping with the
target package and validate timing against the actual Piper voice.

## Performance measurement

Set a budget for the first chosen hardware and renderer before optimisation.
Measure frame time, memory or VRAM, draw calls, triangles, material count,
texture memory and animation cost using that runtime's profiling tools.
Cross-engine budget tables are planning inputs, not verified project results.

## Automation status

Routine GitHub-hosted CI does not validate engine imports. Manual workflow files
may exist as guarded entry points, but a workflow run alone is not acceptance
evidence. Engine validation is complete only when the relevant checks above are
recorded for the exported avatar.
