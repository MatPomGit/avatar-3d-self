# Documentation

This directory contains maintained technical sources of truth. The project is
an early-stage editable production pipeline, not a completed automated avatar
generator.

## Start here

- [Architecture](ARCHITECTURE.md): boundaries, asset lifecycle and canonical
  interchange formats.
- [Roadmap](ROADMAP.md): milestones, acceptance criteria and current blockers.
- [Changelog](../CHANGELOG.md): released baseline and unreleased changes.
- [Architecture decision records](adr/README.md): stable technical decisions.

## Production and tools

- [Complete production pipeline](complete-pipeline.md): manual workflow and
  quality gates.
- [Realistic avatar guide](realistic_avatar_guide.md): capture, topology, rig
  and animation principles.
- [Engine integration](engine-integration.md): target-engine responsibilities.
- [Model format converter](model_format_converter.md): authoritative CLI and
  limitations.
- [Format conversion examples](format_conversion_examples.md): loss-aware
  recipes.

## Execution environments

| Environment | Responsibility | Not performed in GitHub-hosted CI |
| --- | --- | --- |
| Python 3.11 | utilities, tests and static validation | DCC conversion |
| Blender workstation | conversion, texture and rig inspection | Blender execution |
| COLMAP workstation | reconstruction from approved captures | reconstruction |
| Unreal/MetaHuman workstation | import, animation and performance validation | engine automation |
| GitHub Pages | static documentation and viewer | source-data processing or secrets |

See [contributor guidance](../AGENTS.md) for personal-data, Git LFS and change
rules.
