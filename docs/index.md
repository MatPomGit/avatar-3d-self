# Avatar 3D Self

Dokumentacja profesjonalnego pipeline'u tworzenia fotorealistycznego, edytowalnego cyfrowego człowieka czasu rzeczywistego.

<div class="avatar-status-grid">
  <div class="avatar-status-card"><strong>Faza</strong>Reference acquisition and pipeline engineering</div>
  <div class="avatar-status-card"><strong>Kanoniczny DCC</strong>Blender</div>
  <div class="avatar-status-card"><strong>Mowa</strong>Piper → phonemes → visemes</div>
  <div class="avatar-status-card"><strong>Aplikacja</strong>Avatar Studio desktop</div>
</div>

## Jak korzystać z dokumentacji

Jeśli rozpoczynasz projekt, przeczytaj kolejno [cele i wymagania](project/goals-and-requirements.md), [architekturę](project/architecture.md) i [przegląd pipeline'u](pipeline/overview.md). Następnie wykonuj etapy 01–21 w podanej kolejności. Każdy etap definiuje wejście, edytowalny artefakt wyjściowy, kontrole jakości i Definition of Done.

!!! important "Rozdzielenie WWW i aplikacji"
    Strona WWW jest wyłącznie dokumentacją. Prowadzenie użytkownika krok po kroku, zapisywanie stanu projektu, uruchamianie narzędzi lokalnych oraz inspekcja wyników należą do aplikacji [Avatar Studio](desktop/architecture.md).

## Główne obszary

- **Capture**: fotografie, ekspresje, pomiary i manifesty.
- **Modeling**: rekonstrukcja, cleanup, retopologia i UV.
- **Look development**: PBR, skóra, oczy, włosy, zarost, ubrania i okulary.
- **Rigging**: ciało, dłonie, twarz i ruch wtórny.
- **Animation**: lokomocja, gesty, gaze, blinking, emotions i idle motion.
- **Speech**: Piper, alignment fonemów, visemy, koartykulacja i synchronizacja.
- **Runtime**: eksport, integracja z silnikiem, LOD i wydajność.
- **Validation**: podobieństwo, deformacja, uncanny valley i testy odbiorcze.

## Zasada jakości

Nie przechodź do kolejnego etapu dlatego, że poprzedni „wygląda dobrze”. Przechodź dalej dopiero po zapisaniu edytowalnego wyniku i zaliczeniu zdefiniowanych kontroli.
