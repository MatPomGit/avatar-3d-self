# Roadmapa

Roadmapa opisuje rozwój produktu i implementacji. Szczegółowy stan stabilizacji znajduje się w [audycie gotowości przed dalszym rozwojem](../project/pre-development-audit.md).

## M0: profesjonalne fundamenty

- [x] Architektura artefaktów i ADR.
- [x] Portal dokumentacji MkDocs Material.
- [x] Rozdzielenie WWW od lokalnego stanu projektu.
- [x] Architektura Avatar Studio.
- [x] Automatyczna kontrola pokrycia dokumentów przez nawigację MkDocs.
- [x] Automatyczna kontrola terminologii.
- [x] Rygorystyczna budowa dokumentacji przez `mkdocs build --strict`.

## M0.5: stabilizacja fundamentu

**Stan: prawie zamknięte.** Podstawowy wykonywalny pipeline i GUI są połączone. Pozostaje praktyczny smoke test end-to-end na prawdziwym mini-zestawie zdjęć i rzeczywistym COLMAP.

- [x] Dokumentacja GUI odpowiada aktualnej implementacji.
- [x] Minimalny pipeline `zdjęcia -> sparse -> dense/fusion/mesh -> Blender inspection -> artefakt i raport`.
- [x] COLMAP dense reconstruction oraz Poisson/Delaunay meshing.
- [x] Tworzenie/otwieranie workspace z GUI.
- [x] Konfiguracja Blender/COLMAP/FFmpeg/Piper z GUI.
- [x] Uruchamianie podstawowych operacji bez CLI.
- [x] Operacje poza głównym wątkiem GUI.
- [x] Anulowanie aktywnego procesu zewnętrznego.
- [x] Historia `tool_runs` i raporty JSON operacji.
- [x] Bramki DoD, waivery i automatyczne unieważnianie etapów zależnych.
- [x] CI obejmujące kod aplikacji desktopowej.
- [x] Headless GUI smoke test w workflow desktopowym.
- [x] Rozbudowane instrukcje krok po kroku dla etapów 02, 03, 04, 05, 06, 12, 16, 20 i 21.
- [x] Fazowe raportowanie postępu operacji COLMAP w GUI.
- [~] Pozostałe rozdziały pipeline'u wymagają doprowadzenia do tego samego poziomu dydaktycznego.
- [ ] Smoke test end-to-end na prawdziwym mini-zestawie zdjęć i rzeczywistym COLMAP.

**DoD M0.5:** użytkownik bez CLI potrafi skonfigurować narzędzia, sprawdzić serię zdjęć, uruchomić rekonstrukcję sparse i dense, uzyskać mesh i raport, anulować operację oraz przejść przez kontrolowaną bramkę jakości. Do pełnego zamknięcia pozostaje realny test end-to-end.

## M1: pozyskiwanie materiału referencyjnego

**Stan:** dokumentacja capture jest rozwinięta, a GUI tworzy manifest i wykonuje podstawową kontrolę kompletności serii zdjęć. Nie steruje jeszcze kamerą ani automatycznym acquisition.

- [x] prywatny workspace;
- [x] dokumentacja fotografii geometrycznej i referencyjnej;
- [x] procedury samodzielnego capture i obracającej się osoby;
- [x] dokumentacja pomiarów antropometrycznych;
- [x] dokumentacja ekspresji i FACS;
- [x] specyfikacja manifestu pozyskiwania danych;
- [x] kreator manifestu capture w GUI;
- [x] automatyczna kontrola minimalnej liczby zdjęć, rozdzielczości i duplikatów przed COLMAP;
- [ ] automatyczna ocena ostrości, ekspozycji i pokrycia kątowego całej sesji;
- [ ] opcjonalna integracja ze sterowanym acquisition kamery.

**DoD:** zatwierdzony pakiet referencji z kontrolą jakości i bez publikowania danych prywatnych.

## M2: model i opracowanie wyglądu

**Stan:** rekonstrukcja COLMAP jest wykonywalna z GUI; dalsze etapy modelarskie nadal wymagają Blender/DCC.

- [x] sparse reconstruction z GUI;
- [x] dense reconstruction, fusion i mesh z GUI;
- [x] interaktywny diagnostyczny podgląd siatek `.obj/.ply/.stl/.glb/.gltf`;
- [~] cleanup: rozbudowana instrukcja + inspekcja Blender, bez automatycznego edytora;
- [~] retopologia: rozbudowana instrukcja + inspekcja Blender, bez automatycznego workflow;
- [~] UV: rozbudowana instrukcja + narzędzia pomocnicze;
- [~] PBR: dokumentacja i narzędzia pomocnicze;
- [~] oczy, jama ustna, włosy i zarost: dokumentacja produkcyjna;
- [~] ubrania i okulary: dokumentacja produkcyjna.

**DoD:** edytowalny model zalicza geometryczne i wizualne kryteria odbiorcze.

## M3: rig i deformacja

**Stan:** specyfikacje są rozwinięte, a sceny Blender można inspektować z GUI. Automatyczne tworzenie rigu nie jest jeszcze funkcją Avatar Studio.

- [x] specyfikacja szkieletu;
- [x] rozbudowana instrukcja rigu ciała;
- [x] specyfikacja rigu dłoni;
- [x] specyfikacja ARKit/FACS;
- [x] dokumentacja ruchu wtórnego;
- [x] rozbudowana instrukcja skinningu;
- [ ] kreator lub kontrolowany workflow riggingu z GUI;
- [ ] automatyczna walidacja semantyczna skeleton/weights względem specyfikacji.

**DoD:** pełny zakres ruchu bez krytycznych artefaktów deformacji.

## M4: zachowanie i mowa

**Stan:** podstawowe operacje Piper i FFmpeg są dostępne z GUI; pełna generacja animacji mowy i zachowania pozostaje w rozwoju.

- [x] adapter Piper dostępny przez GUI;
- [x] normalizacja audio FFmpeg z GUI;
- [x] dokumentacja fonemów, wizemów i koartykulacji;
- [~] skrypty pomocnicze lip-sync;
- [ ] automatyczne `audio -> alignment -> visemes -> animation curves` z GUI;
- [ ] warstwowa integracja mowy, mimiki, spojrzenia i gestów w podglądzie.

**DoD:** naturalny klip zawierający mowę, emocję, spojrzenie i gest.

## M5: środowisko czasu rzeczywistego

**Stan:** dokumentacja eksportu i walidacji runtime została rozbudowana; demonstrator czasu rzeczywistego nadal nie jest końcowym artefaktem produktu.

- [x] dokumentacja Unreal Engine, Unity i Web;
- [x] specyfikacja LOD i budżetu wydajności;
- [x] rozbudowana procedura eksportu i importu kontrolnego;
- [x] rozbudowana procedura walidacji runtime;
- [ ] wybrany profil referencyjnego runtime dla wersji 1.0;
- [ ] demonstrator czasu rzeczywistego;
- [ ] pomiar wydajności na określonym sprzęcie.

**DoD:** stabilne działanie na określonym sprzęcie w ustalonym budżecie.

## M6: Avatar Studio 1.0

- [x] warstwa adapterów Blender/COLMAP/FFmpeg/Piper;
- [x] warstwa `OperationService` z provenance i historią uruchomień;
- [x] bazowy inspektor artefaktów 3D;
- [x] integracja podstawowych operacji narzędzi z GUI;
- [x] kontrolowane bramki jakości i waivery;
- [x] automatyczne unieważnianie wyników zależnych po zmianie artefaktu;
- [x] podgląd obrazów w GUI;
- [x] interaktywny lekki podgląd siatek 3D z obrotem i zoomem;
- [x] raport końcowy projektu w formacie Markdown i JSON;
- [x] fazowe progress reporting dla długich operacji COLMAP;
- [ ] kolejka wielu operacji;
- [ ] pełne operacje produkcyjne dla kolejnych etapów Blender;
- [ ] podpisane wydanie `.exe` dla Windows i build Linux;
- [ ] referencyjny demonstrator czasu rzeczywistego.

**DoD:** użytkownik może przejść cały wspierany pipeline z poziomu Avatar Studio, otrzymując wersjonowane artefakty, raporty walidacji i odtwarzalny eksport bez ręcznego obchodzenia aplikacji tam, gdzie dany etap jest oznaczony jako zautomatyzowany.
