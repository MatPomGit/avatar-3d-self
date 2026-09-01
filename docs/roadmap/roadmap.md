# Roadmapa

Roadmapa opisuje rozwój produktu i implementacji. Warstwa dokumentacji bazowej dla całego 21-etapowego pipeline'u jest opracowana i utrzymywana zgodnie z [mapą dokumentacji](../project/documentation-map.md). Oznacza to kompletność specyfikacji bazowej, nie zakończenie implementacji wszystkich etapów produkcyjnych.

## M0: profesjonalne fundamenty

- [x] Architektura artefaktów i ADR.
- [x] Portal dokumentacji MkDocs Material.
- [x] Rozdzielenie WWW od lokalnego stanu projektu.
- [x] Architektura Avatar Studio.
- [x] Automatyczna kontrola pokrycia dokumentów przez nawigację MkDocs.
- [x] Automatyczna kontrola terminologii.
- [x] Rygorystyczna budowa dokumentacji przez `mkdocs build --strict`.

**DoD:** czysty klon buduje dokumentację, testy i minimalną aplikację desktopową.

## M1: pozyskiwanie materiału referencyjnego

- prywatny workspace;
- fotografie geometryczne i referencyjne;
- pomiary antropometryczne;
- ekspresje i FACS;
- manifest pozyskiwania danych.

**DoD:** zatwierdzony pakiet referencji z kontrolą jakości i bez publikowania danych prywatnych.

## M2: model i opracowanie wyglądu

- rekonstrukcja i czyszczenie siatki;
- retopologia;
- UV i PBR;
- oczy, jama ustna, włosy i zarost;
- ubrania i okulary.

**DoD:** edytowalny model zalicza geometryczne i wizualne kryteria odbiorcze.

## M3: rig i deformacja

- specyfikacja szkieletu;
- rig ciała i dłoni;
- rig twarzy ARKit/FACS;
- ruch wtórny;
- walidacja wiązania skóry z kośćmi.

**DoD:** pełny zakres ruchu bez krytycznych artefaktów deformacji.

## M4: zachowanie i mowa

- warstwowa animacja;
- spojrzenie, mruganie, animacja bezczynności i gesty;
- Piper;
- dopasowanie czasowe fonemów, wizemy i koartykulacja.

**DoD:** naturalny klip zawierający mowę, emocję, spojrzenie i gest.

## M5: środowisko czasu rzeczywistego

- zatwierdzony silnik docelowy;
- LOD i budżet wydajności;
- walidacja importu;
- demonstrator czasu rzeczywistego.

**DoD:** stabilne działanie na określonym sprzęcie w ustalonym budżecie.

## M6: Avatar Studio 1.0

- adaptery Blender/COLMAP/FFmpeg/Piper;
- inspektor artefaktów 3D;
- integracja operacji narzędzi z interfejsem użytkownika;
- podgląd wyników;
- raport końcowy projektu;
- automatyczne unieważnianie wyników zależnych po zmianie artefaktu;
- podpisane wydanie `.exe` dla Windows i build Linux.

**DoD:** użytkownik może przejść cały obsługiwany pipeline z poziomu Avatar Studio, otrzymując wersjonowane artefakty, raporty walidacji i odtwarzalny eksport bez ręcznego obchodzenia aplikacji.
