# Roadmap

Status reflects repository evidence as of 2026-09-01. Dates are intentionally
omitted until capture and target-runtime constraints are fixed.

## M0 — Documentation and reproducible foundations — in progress

- [x] Separate public tooling from workstation-specific production steps.
- [x] Record architecture decisions, release baseline and planned milestones.
- [ ] Repair the Git LFS pointer inconsistency reported for `baner.jpg`.
- [ ] Make every documented command and path part of a link/command audit.

**Exit criteria:** a clean clone, passing deterministic checks and no broken
documentation links or accidental binary modifications.

## M1 — Reference and capture package — planned

- Define consent, retention and private storage for face, body and voice data.
- Capture calibrated multi-view face/body references including neutral and
  expression poses.
- Record physical scale, glasses dimensions and clothing reference.

**Exit criteria:** complete private reference inventory and documented capture
quality accepted by the project owner.

## M2 — Editable avatar master — planned

- Reconstruct and clean high-resolution scan.
- Produce retopology, UVs, component separation, PBR materials, groom and
  glasses as editable DCC assets.
- Validate anatomy and visual likeness under controlled lighting.

**Exit criteria:** editable master passes deformation and material gates.

## M3 — Rig, facial system and speech — planned

- Implement body, hand, eye and facial rig.
- Define and test the ARKit/FACS control mapping.
- Validate the Piper-to-viseme timing pipeline with the trained personal voice.

**Exit criteria:** natural test clips with speech, blinking, gaze, emotions and
gesture layers; no unreviewed placeholder mappings.

## M4 — Target runtime and performance package — planned

- Select a first runtime target and performance budget.
- Export with a loss report, validate in the target engine and integrate the
  static web preview only where appropriate.
- Capture reproducible import, test and rollback instructions.

**Exit criteria:** target demo meets the agreed quality and performance budget.

## Readiness estimate

Before a publishable interactive prototype: approximately 6–10 focused work
packages. The range depends chiefly on capture quality, chosen DCC/engine and
the maturity of the personal Piper voice. It excludes time-intensive artistic
modelling and manual animation review.
