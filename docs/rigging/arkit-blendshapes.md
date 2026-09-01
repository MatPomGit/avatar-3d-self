# ARKit i kształty deformacyjne twarzy

ARKit wykorzystuje zestaw współczynników opisujących obserwowane ruchy twarzy. W Avatar Studio warstwa ARKit jest interfejsem interoperacyjności dla trackingu i wymiany danych. Nie zastępuje anatomicznego rigu i sama obecność 52 kanałów nie gwarantuje naturalnej mimiki.

## Zakres współczynników

Kanoniczny zakres wejściowy to `0..1`:

- `0`: brak aktywacji kanału;
- `0,25`: subtelna aktywacja;
- `0,5`: średnia, wyraźna aktywacja;
- `0,75`: silna aktywacja;
- `1`: zatwierdzone maksimum dla konkretnego awatara.

Wartość 1 nie oznacza maksymalnego fizjologicznego wysiłku człowieka. Oznacza maksimum bezpieczne i wizualnie poprawne w danym profilu postaci.

## Interfejs a implementacja

Jeden współczynnik wejściowy może sterować kilkoma elementami wewnętrznymi. Przykładowo `mouthSmileLeft` może uruchamiać:

- deformację kącika ust;
- uniesienie policzka;
- subtelną zmianę bruzdy nosowo-wargowej;
- korekcję objętości dolnej powieki.

Dzięki temu warstwa ARKit pozostaje prosta, a wewnętrzny rig może być anatomicznie bogatszy.

## Kanały oczu

`eyeLookUp*`, `eyeLookDown*`, `eyeLookIn*` i `eyeLookOut*` powinny sterować przede wszystkim rotacją gałki ocznej. Powieki reagują osobno przez mechanizm śledzenia powiek za ruchem oka.

Przy wartości około 0,5 oko powinno osiągać mniej więcej połowę zatwierdzonego zakresu, a nie maksymalne spojrzenie. Dla większości neutralnych interakcji komfortowy zakres bez współruchu głowy to około ±20-25° poziomo.

## `jawOpen`

`jawOpen` nie powinien być wyłącznie kształtem ust. Powinien mapować się na anatomiczny ruch żuchwy oraz korekcje tkanek miękkich.

Przykładowa interpretacja:

- 0,0-0,1: usta prawie zamknięte;
- 0,2-0,4: niewielkie otwarcie mowy;
- 0,45-0,7: wyraźne otwarcie;
- 0,7-1,0: duże otwarcie, używane rzadziej.

## Symetria i asymetria

Kanały lewy/prawy muszą działać niezależnie. Kopiowanie jednej strony na drugą może być punktem startowym produkcji, ale po walidacji należy zachować naturalne różnice wynikające z anatomii twarzy.

## Kalibracja trackingu

Współczynnik z systemu trackingu nie musi być używany bezpośrednio. Dopuszczalna jest funkcja kalibracyjna:

`w_avatar = f(w_tracking)`

Może ona kompresować zbyt duże wartości lub wzmacniać słabe sygnały. Funkcja powinna być monotoniczna i udokumentowana.

Przykład: jeśli tracking często daje `mouthSmile=0.9`, a awatar wygląda naturalnie przy 0.65, można zastosować łagodną kompresję górnego zakresu zamiast ograniczenia klipem.

## Test kompletności

Dla każdego z 52 kanałów wykonaj test w wartościach:

`0.0, 0.25, 0.5, 0.75, 1.0`.

Sprawdź:

- monotoniczność efektu;
- brak nagłych skoków;
- brak samoprzecięć;
- zachowanie objętości;
- zgodność lewej i prawej strony;
- poprawną współpracę z `jawOpen`, spojrzeniem i mruganiem.

## Definition of Done

Warstwa ARKit jest zatwierdzona, gdy wszystkie 52 kanały są obecne, nazwy są stabilne, wartości 0-1 zachowują się przewidywalnie, kanały asymetryczne są niezależne, a mapping do wewnętrznego rigu jest udokumentowany.