# ADR-0001: Editable master and interchange formats

**Status:** accepted, 2026-09-01

## Context

The avatar must remain editable across reconstruction, retopology, rigging,
materials and animation. Export formats differ in their ability to retain
skinning, morph targets, materials and animation.

## Decision

Keep the native DCC scene and separated source assets as the canonical master.
Use target-specific interchange: FBX for established engine rigging paths,
GLB/glTF for web delivery, and USD/USDZ only after target validation. Produce
and review a conversion report at each lossy boundary.

## Consequences

Exports are deliverables, not source of truth. The repository must not claim a
conversion is lossless merely because the target format nominally supports it.
