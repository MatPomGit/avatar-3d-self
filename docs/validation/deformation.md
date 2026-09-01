# Walidacja deformacji

Walidacja deformacji sprawdza, czy geometria zachowuje się wiarygodnie w pełnym zakresie animacji. Nie oceniamy jedynie pozy spoczynkowej. Stosujemy macierz póz oraz kombinacje ruchów, ponieważ wiele błędów pojawia się dopiero przy jednoczesnym działaniu kilku stawów lub kanałów twarzy.

## Poziomy oceny

Każdy test otrzymuje wynik:

- **pass**: brak widocznego problemu;
- **warning**: niewielki problem w skrajnym zakresie;
- **fail**: błąd widoczny w zakresie używanym w środowisku czasu rzeczywistego.

## Obręcz barkowa

Testuj zgięcie i odwiedzenie ramienia:

`0°, 45°, 90°, 120°, 150°`.

Dodatkowo testuj rotację ramienia ±30° i ±60° przy 90° uniesienia.

Kryteria:

- bark zachowuje objętość;
- pacha nie tworzy dziury ani ostrego grzbietu;
- obojczyk reaguje na wysokie uniesienie;
- szyja nie jest ciągnięta przez ramię;
- ubranie nie przenika skóry w typowym zakresie.

## Łokieć i przedramię

Łokieć:

`0°, 45°, 90°, 130°`.

Przedramię:

pronacja/supinacja około `±80°`.

Krytyczne są zachowanie łuku łokcia, fałd kompresyjny i brak spiralnego skrętu przedramienia.

## Dłoń

Testuj:

- pełną pięść;
- wskazywanie;
- chwyt cylindryczny;
- chwyt szczypcowy;
- chwyt sferyczny;
- opozycję kciuka;
- rozstaw palców;
- każdy palec osobno.

Fail, jeśli kostki zapadają się, opuszki tracą objętość lub błony międzypalcowe rozrywają się.

## Kręgosłup

Testuj skłon, wyprost, skłon boczny oraz skręt około ±30° i ±45°. Dodaj kombinację skrętu z podniesionymi ramionami.

## Biodro i kolano

Biodro:

`0°, 45°, 90°, 120°` zgięcia.

Kolano:

`0°, 45°, 90°, 130°`.

Dodaj głęboki przysiad. Pachwina i pośladek powinny zachować masę, a kolano nie może tworzyć ostrego przewężenia.

## Twarz

Każdy kanał twarzy testuj przy:

`0.0, 0.25, 0.5, 0.75, 1.0`.

Następnie testuj kombinacje:

- `jawOpen + mouthSmile`;
- `jawOpen + mouthPucker`;
- `jawOpen + mouthFunnel`;
- `eyeBlink + eyeLookUp/Down`;
- `cheekSquint + eyeBlink`;
- `browDown + eyeSquint`;
- asymetryczny uśmiech;
- lip-sync + mruganie + ruch oczu.

## Kształty korekcyjne

Kształt korekcyjny jest wymagany, gdy poprawa samych wag pogarsza inną pozę lub nie jest w stanie zachować objętości.

Każdy corrective musi mieć:

- jawny warunek aktywacji;
- zakres wpływu;
- test pozy pośredniej;
- test regresyjny.

## Penetracje

Widoczna penetracja skóry, oka, zębów, języka lub odzieży w typowej pozie to fail. Drobna kolizja poniżej około 1 mm może być warning tylko w ekstremalnej pozie, która nie występuje w docelowej animacji.

## Macierz testowa

Raport powinien zawierać co najmniej:

| Pole | Znaczenie |
| --- | --- |
| `region` | bark, łokieć, dłoń, biodro, twarz itd. |
| `pose` | nazwa pozy |
| `value` | kąt lub waga kanału |
| `result` | pass/warning/fail |
| `artifact` | opis błędu |
| `cause` | wagi, topologia, rig, corrective |
| `fix` | zastosowana poprawka |
| `regression_passed` | wynik ponownego testu |

## Definition of Done

Deformacja jest zatwierdzona, gdy wszystkie obowiązkowe pozy i kombinacje przechodzą bez błędów w zakresie produkcyjnym, a wszystkie warnings są udokumentowane jako świadome ograniczenia.