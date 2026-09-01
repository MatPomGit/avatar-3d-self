# Profil fonemów języka polskiego

Ten dokument definiuje warstwę roboczą między zapisem fonetycznym a animacją ust dla języka polskiego. Celem nie jest stworzenie pełnego podręcznika fonetyki, lecz zapewnienie stabilnej klasyfikacji potrzebnej do synchronizacji ruchu ust z mową.

## Dlaczego potrzebny jest profil

Różne narzędzia mogą zapisywać ten sam dźwięk innym symbolem. eSpeak NG używa własnej notacji fonemicznej, podczas gdy publikacje językoznawcze często stosują międzynarodowy alfabet fonetyczny IPA. Avatar Studio nie powinno uzależniać animacji od jednego zapisu.

Dlatego pipeline ma trzy warstwy:

```text
symbol narzędzia → kanoniczna klasa fonetyczna → wizem
```

## Samogłoski

Dla animacji samogłoski opisujemy głównie przez stopień otwarcia żuchwy oraz zaokrąglenie i rozciągnięcie ust.

| Przykład ortograficzny | Przybliżona kategoria | Wizem bazowy | Charakter ruchu |
| --- | --- | --- | --- |
| a | otwarta centralna | AA | duże otwarcie żuchwy |
| e | średnio otwarta przednia | E | umiarkowane otwarcie, usta szerzej |
| i | wysoka przednia | I | małe otwarcie, rozciągnięte kąciki |
| y | wysoka centralno-tylna | I/E blend | małe otwarcie bez silnego uśmiechu |
| o | średnio otwarta tylna | O | wyraźne zaokrąglenie |
| u/ó | wysoka tylna | U | silniejsze wysunięcie i zwężenie warg |

Wartości są celami animacyjnymi, a nie twierdzeniem o identyczności fonetycznej głosek.

## Spółgłoski wargowe

`/p b m/` wymagają pełnego domknięcia warg i mapują się do wizemu `PP`.

`/f v/` wymagają kontaktu dolnej wargi z górnymi zębami i mapują się do `FF`.

Dla `PP` kontakt geometryczny ma wyższy priorytet niż wygładzanie. Nawet krótki fonem powinien osiągnąć czytelne domknięcie, jeśli jest akcentowany.

## Spółgłoski przedniojęzykowe

Dźwięki odpowiadające m.in. `t`, `d`, `n`, `l` wymagają ruchu przedniej części języka, ale zewnętrzny kształt ust zmienia się niewiele. W praktyce bazą jest wizem `DD`, a najważniejsza animacja zachodzi wewnątrz jamy ustnej.

## Spółgłoski szczelinowe i syczące

Dźwięki z grup `s`, `z`, `c`, `dz` oraz pokrewne wymagają wąskiej szczeliny i niewielkiego otwarcia żuchwy. Bazą jest `SS` albo mieszanie `SS` z `CH` zależnie od miejsca artykulacji.

Dla `sz`, `ż/rz`, `cz`, `dż` usta są zwykle nieco bardziej zaokrąglone niż dla `s/z`, dlatego wzrasta udział `CH`.

## Spółgłoski miękkie

Dźwięki zapisywane m.in. jako `ś`, `ź`, `ć`, `dź`, `ń` wymagają zmian głównie języka. Zewnętrzny kształt ust jest zwykle subtelniejszy niż w angielskim `sh/ch`. Profil powinien więc unikać przesadnego wysuwania warg.

## Spółgłoski tylnojęzykowe

`k`, `g`, `ch/h` mapują się głównie do `KK`. Ruch języka znajduje się głęboko w jamie ustnej, dlatego żuchwa i usta powinny przede wszystkim przygotować przejście do sąsiedniej samogłoski.

## Fonem r

Polskie `r` nie powinno być animowane przez silny ruch samych warg. Wizem `RR` jest przede wszystkim neutralnym stanem ust z kontrolą języka. W szybkiej mowie jego zewnętrzna amplituda może być bardzo mała.

## Koartykulacja

Koartykulacja (coarticulation) powoduje, że kształt ust dla danego fonemu jest modyfikowany przez sąsiednie fonemy. Na przykład w sekwencji „tu” zaokrąglenie warg dla `/u/` zaczyna się jeszcze podczas poprzedniej spółgłoski.

Dla polskiego profilu zachowujemy domyślne narastanie 50-80 ms i wygaszanie 80-120 ms, ale kontaktowe `PP` i `FF` mogą tymczasowo przejąć priorytet nad sąsiednią samogłoską.

## Walidacja profilu

Minimalny korpus testowy powinien zawierać:

- `pa ba ma fa wa`;
- `ta da na la`;
- `ka ga ha`;
- `sa za ca dza`;
- `sza ża cza dża`;
- `sia zia cia dzia nia`;
- sekwencje samogłosek `a-e-i-o-u-y`;
- zdania zawierające szybkie przejścia spółgłoska-samogłoska.

Każdy test oceniamy z dźwiękiem i bez dźwięku. Bez dźwięku ruch nadal powinien wyglądać jak wiarygodna artykulacja, a nie losowe otwieranie ust.
