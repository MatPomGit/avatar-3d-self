# Struktura repozytorium

```text
apps/avatar_studio/     desktop GUI and local orchestration
docs/                   MkDocs documentation and specifications
scripts/                deterministic CLI tooling
references/             public-safe manifests, never raw biometric data
source/                 approved editable source assets and descriptors
animations/             animation and mapping metadata
exports/                derived interchange files and conversion reports
tests/                  automated tests
.github/workflows/       CI, documentation and packaging workflows
```

## Zasady odpowiedzialności

`docs/` nie zawiera logiki stanu projektu. `apps/avatar_studio/` nie duplikuje treści technicznej z dokumentacji, lecz wiąże definicje etapów z interfejsem i wynikami. `scripts/` zawiera funkcje możliwe do uruchomienia bez GUI, dzięki czemu CI i aplikacja korzystają z tego samego zachowania.

Duże pliki źródłowe mogą być wersjonowane przez Git LFS tylko wtedy, gdy są przeznaczone do publikacji. Prywatne zdjęcia, głos i skany pozostają w lokalnym workspace poza repozytorium.
