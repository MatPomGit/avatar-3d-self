# Przegląd pipeline'u

Pipeline jest sekwencją kontrolowanych transformacji artefaktów. Kolejny etap może rozpocząć się dopiero wtedy, gdy wymagane wejścia mają status `approved`.

```text
01 references
  ↓
02 photogrammetry
  ↓
03 reconstruction
  ↓
04 high-poly cleanup
  ↓
05 retopology ─────────────── topology freeze
  ↓
06 UV
  ↓
07 PBR ── 08 eyes ── 09 hair ── 10 clothing ── 11 glasses
  ↓
12 body rig ── 13 hand rig ── 14 facial rig
  ↓
15 secondary motion
  ↓
16 skinning and deformation approval
  ↓
17 layered animation
  ↓
18 lip-sync ── 19 Piper
  ↓
20 export
  ↓
21 runtime validation
```

## Gate jakości

Każdy etap kończy się raportem. Minimalny raport zapisuje wersję narzędzia, wejścia, wyjścia, hash artefaktu, wyniki kontroli i odstępstwa. Status `passed` oznacza, że spełniono DoD, a nie tylko ukończono operację w programie.

## Topology freeze

Po zatwierdzeniu etapu 05 nie zmieniaj kolejności i liczby wierzchołków bez utworzenia nowej wersji bazowego mesha i ponownej walidacji wszystkich zależnych shape keys, skinningu, groom attachment oraz ubrań.

## Mapa decyzyjna

| Decyzja | Odpowiedź |
| --- | --- |
| Wymagane wejście | Dla etapu 01: prywatny lub syntetyczny zestaw referencji, zgody i workspace poza repozytorium. Dla każdego kolejnego etapu: wyłącznie wymagane artefakty upstream o statusie `approved`. |
| Kolejność lektury | Najpierw bieżący artykuł numerowany 01–21, następnie wskazane w nim dokumenty dziedzinowe; nie pomijaj kolejności strzałek z diagramu. |
| Rezultat | Edytowalny artefakt etapu, pochodne podglądy lub eksporty, metadane provenance i raport walidacji; na końcu zwalidowany pakiet runtime. |
| Przejście dalej | Definition of Done bieżącego etapu ma status `passed`, oficjalne wyjście jest `approved`, a raport zawiera wejścia, wyjścia, wersje narzędzi i SHA-256. |
| Gdy warunek nie jest spełniony | Po `failed` zatrzymaj etapy downstream, zachowaj ostatni artefakt `approved` i przejdź do [diagnostyki](../desktop/troubleshooting.md). Po naprawie powtórz kontrolę; nie edytuj ręcznie bazy projektu. |
