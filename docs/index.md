# Avatar Studio

**Avatar Studio** to pipeline i aplikacja desktopowa do tworzenia fotorealistycznego, edytowalnego cyfrowego człowieka czasu rzeczywistego.

## Od czego zacząć

Dla nowego projektu zacznij od [przeglądu projektu](project/overview.md). Avatar Studio prowadzi stan 21 etapów i pomaga uruchamiać wybrane narzędzia, ale nie tworzy samodzielnie gotowego człowieka. Wynikiem pracy jest edytowalna scena wzorcowa, materiały, rig i animacje oraz zwalidowany pakiet do wybranego środowiska czasu rzeczywistego. Modelowanie, retopologia, UV, materiały, włosy, ubrania, rig, skinning i animacja wymagają nadal pracy autora w programie DCC.

### Ścieżka pierwszego projektu

1. Przeczytaj konfigurację dla [Windows](setup/windows.md) albo [Linux](setup/linux.md), a przed dodaniem materiałów — [zasady prywatności](project/privacy-and-reference-data.md).
2. Poznaj [przechwytywanie materiału](capture/photography-guide.md), [modelowanie](modeling/overview.md), [rig](rigging/skeleton-specification.md), [materiały](materials/overview.md), [animację](animation/animation-architecture.md), [eksport](runtime/overview.md) i [walidację](validation/acceptance-criteria.md), dokładnie w tej kolejności. [Przegląd pipeline'u](pipeline/overview.md) łączy te obszary z 21 etapami wykonawczymi.
3. Utwórz lokalny workspace według [instrukcji GUI](desktop/user-workflow.md#1-utworzenie-lub-otwarcie-projektu). Wybierz katalog poza klonem repozytorium; obecność `.avatar-studio/project.sqlite3` i `reports/` w wybranym katalogu oraz brak tych elementów w repozytorium potwierdzają właściwe rozdzielenie.
4. Pierwsze przejście wykonaj na syntetycznych renderach nieprzedstawiających rzeczywistej osoby: zarejestruj serię w etapie 01, sprawdź manifest i — jeśli ujęcia mają wystarczające pokrycie — przetestuj etapy 02–03. To próba mechaniki workspace, raportów i bramek, a nie odbiór jakości człowieka.
5. Zatrzymaj się po każdym etapie na bramce jakości. Po wyniku `failed` nie uruchamiaj etapów zależnych ani nie używaj wadliwego artefaktu jako wejścia; przejdź do [diagnostyki](desktop/troubleshooting.md), usuń przyczynę i powtórz walidację.
6. Gdy korekta pogarsza wynik, wróć do ostatniego artefaktu ze statusem `approved`, wskazanego wersją i SHA-256 w raporcie. Pracuj na jego nowej kopii `vNNN`, zamiast nadpisywać zatwierdzony plik; szczegóły opisuje [wersjonowanie artefaktów](project/asset-versioning.md).

!!! warning "Dane prywatne"
    Zdjęcia, skany, nagrania i modele głosu są danymi identyfikującymi. Nie kopiuj ich do repozytorium, katalogu publikowanej dokumentacji ani niezaufanej synchronizacji chmurowej.

Materiał zdjęciowy: [Photography guide](capture/photography-guide.md) oraz [Self capture](capture/self-capture.md).

Rozwój aplikacji: [architektura Avatar Studio](desktop/architecture.md), [workspace projektu](desktop/project-workspace.md) i [inspekcja artefaktów](desktop/artifact-inspection.md).

!!! important "WWW i aplikacja"
    Strona WWW jest dokumentacją techniczną i dydaktyczną. Stan projektu, lokalne uruchamianie narzędzi i inspekcja wyników należą do aplikacji Avatar Studio.

## Obszary dokumentacji

- [Capture](capture/photography-guide.md): zdjęcia, pomiary, ekspresje i manifesty.
- [Modeling](modeling/overview.md): anatomia, retopologia, topologia twarzy, dłonie, stopy i jama ustna.
- [Materials](materials/overview.md): PBR, skóra, oczy, włosy, zarost i ubrania.
- [Rigging](rigging/skeleton-specification.md): skeleton, ciało, dłonie, twarz, ARKit, FACS i ruch wtórny.
- [Animation](animation/animation-architecture.md): locomotion, gestures, gaze, blinking, emotions i idle.
- [Speech](speech/architecture.md): Piper, fonemy, visemy, koartykulacja i facial curves.
- [Runtime](runtime/overview.md): eksport, LOD, wydajność i integracja z silnikiem.
- [Validation](validation/acceptance-criteria.md): podobieństwo, geometria, deformacja, uncanny valley i performance.

## Kontrakt każdego etapu

Każdy etap powinien pozostawić jawne wejście, edytowalny artefakt źródłowy, artefakty pochodne, metadane, raport walidacji i spełnione Definition of Done.

Nie przechodź dalej tylko dlatego, że wynik wygląda poprawnie. Avatar Studio ma pokazywać, dlaczego etap został zaliczony albo zablokowany.

## Kluczowe dokumenty

- [Production pipeline](pipeline/overview.md)
- [Photography guide](capture/photography-guide.md)
- [Topology](modeling/topology.md)
- [PBR conventions](materials/pbr-conventions.md)
- [Facial rig specification](rigging/facial-rig-specification.md)
- [Animation architecture](animation/animation-architecture.md)
- [Speech architecture](speech/architecture.md)
- [Acceptance criteria](validation/acceptance-criteria.md)
- [Avatar Studio architecture](desktop/architecture.md)
- [Roadmap](roadmap/roadmap.md)
