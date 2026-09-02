# Roadmapa

Roadmapa opisuje rozwój produktu i implementacji. Warstwa dokumentacji bazowej dla całego 21-etapowego pipeline'u jest opracowana i utrzymywana zgodnie z [mapą dokumentacji](../project/documentation-map.md). Oznacza to kompletność specyfikacji bazowej, nie zakończenie implementacji wszystkich etapów produkcyjnych.

Stan implementacji po audycie opisuje [audyt gotowości przed dalszym rozwojem](../project/pre-development-audit.md). Obecna aplikacja desktopowa jest przede wszystkim nawigatorem pipeline'u i rejestrem artefaktów. Adaptery Blender/COLMAP/FFmpeg/Piper istnieją, ale większość operacji nie jest jeszcze dostępna z GUI.

## M0: profesjonalne fundamenty

- [x] Architektura artefaktów i ADR.
- [x] Portal dokumentacji MkDocs Material.
- [x] Rozdzielenie WWW od lokalnego stanu projektu.
- [x] Architektura Avatar Studio.
- [x] Automatyczna kontrola pokrycia dokumentów przez nawigację MkDocs.
- [x] Automatyczna kontrola terminologii.
- [x] Rygorystyczna budowa dokumentacji przez `mkdocs build --strict`.

**DoD:** czysty klon buduje dokumentację, testy i minimalną aplikację desktopową.

## M0.5: stabilizacja fundamentu

Ten kamień milowy jest warunkiem przejścia od architektury demonstracyjnej do podstawowego produktu używalnego bez ręcznego wpisywania poleceń.

- [ ] Uzgodnić dokumentację GUI z faktyczną implementacją i jawnie oznaczać funkcje `implemented`, `partial` oraz `planned`.
- [ ] Zdefiniować i uruchomić minimalny pipeline `zdjęcia -> sparse reconstruction -> dense/mesh -> inspekcja Blender -> artefakt i raport`.
- [ ] Dodać dense reconstruction i meshing albo jawnie zintegrować wspierane narzędzie zastępcze.
- [ ] Dodać kreator projektu oraz konfigurację Blender/COLMAP/FFmpeg/Piper w GUI.
- [ ] Udostępnić formularze i przyciski uruchamiające adaptery bez konieczności używania CLI.
- [ ] Uruchamiać długie zadania poza wątkiem UI z postępem, logiem, błędami i anulowaniem.
- [ ] Wprowadzić rzeczywiste bramki Definition of Done, kontrolowane wyjątki i unieważnianie zależnych wyników.
- [ ] Rozbudować najkrótsze rozdziały pipeline'u do instrukcji dydaktycznych krok po kroku.
- [ ] Rozszerzyć CI o kod aplikacji desktopowej i usunąć puste testy/artefakty sugerujące nieistniejącą kompletność.

**DoD:** użytkownik bez wpisywania poleceń tworzy projekt, konfiguruje narzędzia, uruchamia podstawową rekonstrukcję, obserwuje postęp, otrzymuje artefakt i raport oraz przechodzi dalej wyłącznie po spełnieniu kryteriów jakości lub zapisaniu jawnego wyjątku.

## M1: pozyskiwanie materiału referencyjnego

**Stan:** dokumentacja i struktura danych są rozwinięte; pełna obsługa procesu przez GUI pozostaje częściowa.

- prywatny workspace;
- fotografie geometryczne i referencyjne;
- pomiary antropometryczne;
- ekspresje i FACS;
- manifest pozyskiwania danych.

**DoD:** zatwierdzony pakiet referencji z kontrolą jakości i bez publikowania danych prywatnych.

## M2: model i opracowanie wyglądu

**Stan:** dokumentacja i część narzędzi pomocniczych istnieją; pełny workflow produkcyjny nie jest jeszcze zintegrowany z Avatar Studio.

- rekonstrukcja i czyszczenie siatki;
- retopologia;
- UV i PBR;
- oczy, jama ustna, włosy i zarost;
- ubrania i okulary.

**DoD:** edytowalny model zalicza geometryczne i wizualne kryteria odbiorcze.

## M3: rig i deformacja

**Stan:** istnieją specyfikacje i walidatory pomocnicze; wykonanie i kontrola pełnego rigu nadal wymagają pracy w narzędziu DCC.

- specyfikacja szkieletu;
- rig ciała i dłoni;
- rig twarzy ARKit/FACS;
- ruch wtórny;
- walidacja wiązania skóry z kośćmi.

**DoD:** pełny zakres ruchu bez krytycznych artefaktów deformacji.

## M4: zachowanie i mowa

**Stan:** istnieją adapter Piper, dokumentacja fonemów/wizemów i skrypty pomocnicze; brak kompletnego sterowania tym procesem z GUI.

- warstwowa animacja;
- spojrzenie, mruganie, animacja bezczynności i gesty;
- Piper;
- dopasowanie czasowe fonemów, wizemy i koartykulacja.

**DoD:** naturalny klip zawierający mowę, emocję, spojrzenie i gest.

## M5: środowisko czasu rzeczywistego

**Stan:** dokumentacja eksportu i walidacji istnieje; demonstrator czasu rzeczywistego nie jest jeszcze końcowym, zweryfikowanym artefaktem produktu.

- zatwierdzony silnik docelowy;
- LOD i budżet wydajności;
- walidacja importu;
- demonstrator czasu rzeczywistego.

**DoD:** stabilne działanie na określonym sprzęcie w ustalonym budżecie.

## M6: Avatar Studio 1.0

- [x] bazowa warstwa adapterów Blender/COLMAP/FFmpeg/Piper;
- [~] bazowy inspektor artefaktów 3D, wymagający pogłębienia dla scen, rigu, materiałów i animacji;
- [ ] integracja operacji narzędzi z interfejsem użytkownika;
- [ ] podgląd wyników;
- [ ] raport końcowy projektu;
- [ ] automatyczne unieważnianie wyników zależnych po zmianie artefaktu;
- [ ] podpisane wydanie `.exe` dla Windows i build Linux.

**DoD:** użytkownik może przejść cały obsługiwany pipeline z poziomu Avatar Studio, otrzymując wersjonowane artefakty, raporty walidacji i odtwarzalny eksport bez ręcznego obchodzenia aplikacji.
