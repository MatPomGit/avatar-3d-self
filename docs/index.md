# Avatar Studio

**Avatar Studio** to pipeline i aplikacja desktopowa do tworzenia fotorealistycznego, edytowalnego cyfrowego człowieka czasu rzeczywistego.

## Od czego zacząć

Dla nowego projektu przeczytaj kolejno [cele i wymagania](project/goals-and-requirements.md), [architekturę](project/architecture.md) oraz [przegląd pipeline'u](pipeline/overview.md).

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
