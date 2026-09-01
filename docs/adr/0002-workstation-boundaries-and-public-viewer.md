# ADR-0002: Workstation boundaries and public viewer

**Status:** accepted, 2026-09-01

## Context

COLMAP, Blender, MetaHuman, Unreal Engine and a personal Piper installation are
large, licensed or locally configured environments. Raw reference and voice data
are sensitive.

## Decision

Use GitHub Actions only for deterministic source checks and static-site
deployment. Keep specialist processing manual until a reproducible dedicated
runner and approved test assets exist. Publish only a static viewer and
non-sensitive documentation through GitHub Pages.

## Consequences

Manual workflows must state prerequisites and validation gates. Credentials and
source photos, scans and voice recordings never enter the public web bundle or
routine CI.
