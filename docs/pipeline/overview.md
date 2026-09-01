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
