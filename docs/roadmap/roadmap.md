# Roadmapa

## M0: profesjonalne fundamenty

- [x] Architektura artefaktów i ADR.
- [x] Portal dokumentacji MkDocs Material.
- [x] Rozdzielenie WWW od lokalnego stanu projektu.
- [x] Architektura Avatar Studio.
- [ ] Pełny audyt lokalnych linków i manifestów w CI.

**DoD:** czysty klon buduje dokumentację, testy i minimalną aplikację desktopową.

## M1: capture

- prywatny workspace;
- fotografie geometryczne i referencyjne;
- pomiary antropometryczne;
- ekspresje i FACS;
- capture manifest.

**DoD:** zatwierdzony pakiet referencji z kontrolą jakości i bez publikowania danych prywatnych.

## M2: model i look development

- rekonstrukcja i cleanup;
- retopologia;
- UV i PBR;
- oczy, jama ustna, włosy i zarost;
- ubrania i okulary.

**DoD:** edytowalny model zalicza geometryczne i wizualne kryteria odbiorcze.

## M3: rig i deformacja

- skeleton specification;
- body and hand rig;
- facial rig ARKit/FACS;
- secondary motion;
- skinning validation.

**DoD:** pełny zakres ruchu bez krytycznych artefaktów deformacji.

## M4: zachowanie i mowa

- warstwowa animacja;
- gaze, blinking, idle i gestures;
- Piper;
- phoneme alignment, visemes i coarticulation.

**DoD:** naturalny klip zawierający mowę, emocję, gaze i gest.

## M5: runtime

- zatwierdzony target engine;
- LOD i performance budget;
- import validation;
- demonstrator czasu rzeczywistego.

**DoD:** stabilne działanie na określonym sprzęcie w ustalonym budżecie.

## M6: Avatar Studio 1.0

- adaptery Blender/COLMAP/Piper;
- inspektor artefaktów 3D;
- preview wyników;
- raport końcowy projektu;
- podpisane wydanie `.exe` dla Windows i build Linux.
