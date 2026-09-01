# Wersjonowanie artefaktów

## Nazwy

Przykładowe nazwy stabilnych punktów pracy:

```text
avatar_body_scan_v001.ply
avatar_body_clean_v003.blend
avatar_body_retopo_v012.blend
avatar_skin_v006.spp
avatar_face_rig_v007.blend
avatar_groom_v004.blend
avatar_runtime_v002.fbx
```

Numer wersji zwiększaj, gdy wynik staje się nowym punktem odniesienia dla następnego etapu. Nie twórz wersji po każdej drobnej operacji.

## Status artefaktu

Każdy artefakt ma jeden status: `working`, `candidate`, `approved`, `superseded`, `rejected`. Tylko `approved` może być oficjalnym wejściem następnego etapu.

## Manifest

Raport etapu powinien rejestrować co najmniej:

```json
{
  "artifact_id": "body_retopo",
  "version": 12,
  "status": "approved",
  "source": "avatar_body_clean_v003.blend",
  "tool": "Blender",
  "tool_version": "4.x",
  "sha256": "...",
  "validation_report": "reports/retopology_v012.json"
}
```

## Zmiany łamiące zależności

Zmiana liczby lub kolejności wierzchołków głównej siatki po rozpoczęciu facial shapes lub skinningu jest breaking change. Należy wtedy utworzyć nową linię wersji zależnych artefaktów i ponownie wykonać ich walidację.
