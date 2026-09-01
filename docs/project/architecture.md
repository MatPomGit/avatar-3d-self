# Architektura projektu

## Przepływ artefaktów

```text
private references
      ↓
capture manifest
      ↓
reconstruction / scan
      ↓
clean high-poly
      ↓
retopologized base mesh
      ├── UV + PBR
      ├── eyes / teeth / tongue
      ├── hair / beard
      ├── clothing / glasses
      └── skeleton + skinning
                ↓
          facial rig / shapes
                ↓
           animation layers
                ↓
Piper → phonemes → visemes → speech curves
                ↓
        validated runtime export
```

## Asset dependency graph

Topologia głównego mesha jest punktem stabilizacji. Rig, skinning, shape keys, groom attachment i część ubrań zależą od indeksów lub położenia wierzchołków. Zmiana topologii po rozpoczęciu tych prac musi być traktowana jako migracja, a nie zwykła korekta.

## Kontrakty etapów

Każdy etap definiuje:

- **Input**: wymagane artefakty i ich minimalny stan;
- **Process**: operacje wykonywane na kopii roboczej;
- **Editable output**: kanoniczny wynik do dalszej edycji;
- **Derived output**: eksporty, preview i raporty;
- **Validation**: kontrole automatyczne i manualne;
- **Failure conditions**: błędy blokujące kolejny etap;
- **Definition of Done**: jednoznaczny warunek zamknięcia etapu.

## Granice wykonawcze

Blender, COLMAP, Piper i silniki działają lokalnie. CI wykonuje tylko lekkie, deterministyczne kontrole kodu, dokumentacji, manifestów i raportów. Avatar Studio może uruchamiać narzędzia lokalne przez adaptery procesu, ale nie przechowuje binariów tych narzędzi.

## Format i jednostki

Kanoniczna scena DCC zachowuje skalę rzeczywistą. Eksport do Unreal jest walidowany w centymetrach, a każdy format pośredni ma jawny raport jednostek, osi, skeletonu, morph targets i materiałów.
