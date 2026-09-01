# ADR-0003: Facial-control and speech interface

**Status:** accepted, 2026-09-01

## Context

Natural speech cannot be obtained reliably by driving a face only from audio
amplitude. The facial rig must also remain compatible with face tracking and
expressive animation.

## Decision

Use a documented facial-control layer compatible with ARKit blendshape names,
FACS semantics or an explicit mapping between them. Drive speech from
phoneme/viseme timing derived alongside Piper audio, then layer it with jaw,
gaze, blinks, asymmetry, head motion and emotion controls.

## Consequences

Every target export must include or reference its mapping. A viseme generator is
an integration helper, not proof of timing accuracy; validate it against the
actual voice and runtime.
