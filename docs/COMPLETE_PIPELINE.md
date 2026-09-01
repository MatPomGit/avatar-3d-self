# Complete avatar production pipeline

This is the intended editable production workflow. A check mark is earned only
after the stated quality gate is recorded for the actual avatar; it is not
implied by the presence of a script or a GitHub Actions workflow.

## 1. Reference capture and consent

Capture consistent facial, profile, three-quarter, full-body and clothing
references. Record lighting, focal length, scale reference and intended use.
Keep raw images, scans, audio and biometric annotations outside this public
repository unless explicit publication approval exists.

**Gate:** sufficient multi-view coverage, neutral expression and a reference
inventory; the distinctive face, glasses and facial hair are visible.

## 2. Reconstruction and editable high-resolution source

Use a local COLMAP or comparable workflow to create a dense scan. Clean only
reconstruction artefacts in a high-resolution source mesh; retain original
capture and unmodified reconstruction separately.

**Gate:** correct scale and orientation, no missing facial regions, and no
destructive overwrite of the source scan.

## 3. Retopology, UVs and component separation

Create animation-ready topology with loops around eyelids, mouth, jaw, cheeks,
shoulders, elbows, wrists, hips, knees and fingers. Keep body, teeth, tongue,
eyes, glasses, clothing and hair/groom as separate editable components.

**Gate:** clean deformation test for blink, jaw open, smile, fist, shoulder
raise, elbow bend and knee bend.

## 4. Materials, hair, clothing and glasses

Prepare PBR maps appropriate to each component. Skin requires believable colour
variation, micro-normal detail and, where supported, subsurface scattering.
Hair and beard require groom or suitable cards, not merely a flat colour map.
The provided `pbr_texture_processor.py` is a utility and does not replace
material review in the target renderer.

**Gate:** inspected under neutral and raking light; glasses preserve frame and
lens behaviour; no visible seams or texture stretching.

## 5. Body, hand and facial rig

Build an IK/FK body rig, individual finger controls, independent eye aim and a
facial system compatible with the chosen ARKit/FACS mapping.

**Gate:** correct skinning through the deformation set and a validated mapping
for every implemented facial control.

## 6. Speech and behaviour layers

The target chain is `text -> Piper audio -> phoneme/viseme timing -> facial
animation -> engine playback`. `scripts/piper_lipsync_generator.py` is an
experimental helper: validate its Piper invocation and timing output against the
installed voice before relying on it. Layer visemes with jaw motion, gaze,
blinks, asymmetry, head motion and gestures.

**Gate:** reviewed spoken clips with consonant closures, no eye deadness and no
audio-animation drift.

## 7. Export and target validation

Use the format converter with a report and `--strict` when a loss is not
acceptable. Keep a high-fidelity editable master and create target-specific
exports. Validate the export in the destination application.

**Gate:** geometry, materials, UVs, rig, skin weights, shape keys and animation
are checked after import; intended losses are recorded in the conversion report.

## 8. Real-time integration and release package

Integrate the validated asset in one target runtime first. Measure frame time,
memory, draw calls and visual quality on target hardware. Deliver an asset
manifest, known limitations and reproducible import steps with the export.

**Gate:** the selected runtime can load, idle, speak, emote and gesture without
regressing likeness or the agreed performance budget.

## Automation boundary

GitHub Actions validates deterministic source quality and deploys the static
viewer. Heavy reconstruction, Blender, MetaHuman and Unreal Engine operations
are manual workflow entry points only; they are not routine CI or releases until
a reproducible runner and test assets exist.
