# Specyfikacja układu sterowania twarzą

Układ sterowania twarzą łączy anatomiczne ruchy kości, kształty deformacyjne, ruch oczu, powiek, żuchwy i języka. Warstwą interoperacyjną jest zestaw ARKit, a FACS służy do interpretacji ruchów mięśniowych i walidacji ekspresji.

## Architektura hybrydowa

Preferowany jest rig hybrydowy:

- kości lub transformacje dla żuchwy i oczu;
- kształty deformacyjne dla miękkich tkanek twarzy;
- kształty korekcyjne dla trudnych kombinacji;
- dodatkowe kontrolery dla języka;
- warstwa ARKit jako stabilny interfejs wejściowy.

Takie podejście ogranicza liczbę deformacji, które muszą być ręcznie rzeźbione, a jednocześnie pozwala zachować anatomiczną kontrolę.

## Neutralna twarz

Neutralna poza jest stanem kalibracyjnym. Usta są domknięte bez zaciskania, żuchwa pozostaje w pozycji spoczynkowej, oczy są naturalnie otwarte, a brwi nie są sztucznie uniesione.

Neutral nie może być tworzony przez kompensowanie błędnej geometrii wartościami sterowników.

## Żuchwa

Żuchwa jest sterowana transformem lub kością. `jawOpen=1` odpowiada zatwierdzonemu maksimum awatara, zwykle około 30-35 mm rozwarcia między siekaczami i około 25-30° rotacji.

Ruch boczny może wynosić około 5-8 mm, a wysunięcie około 4-7 mm. Są to wartości orientacyjne. Model referencyjny ma pierwszeństwo.

## Domknięcie warg

Domknięcie warg (lip seal) jest niezależne od zamknięcia żuchwy. Pełna siła może działać do około `jawOpen=0.08`, następnie wygasać płynnie do zera przy około `0.22`.

Zbyt silne domknięcie powoduje wciąganie czerwieni warg do wnętrza. Zbyt słabe daje szczelinę przy `/p b m/`.

## Powieki

Pełne mrugnięcie nie jest prostym przesunięciem górnej powieki. Górna powieka wykonuje większość ruchu, a dolna niewielki ruch współtowarzyszący. Punktem startowym może być około 85% ruchu górnej i 15% dolnej powieki.

Testuj `eyeBlink` przy 0,25, 0,5, 0,75 i 1,0. Oko musi zamknąć się bez penetracji rogówki i bez utraty naturalnego łuku powieki.

## Śledzenie powiek za ruchem oka

Powieki podążają za pionowym ruchem gałki ocznej. Jako punkt startowy przyjmujemy wpływ około 0,30-0,35 dla spojrzenia w górę i 0,40-0,45 dla spojrzenia w dół.

Zbyt mała wartość daje efekt oka poruszającego się niezależnie od powieki. Zbyt duża sprawia, że powieka „przykleja się” do oka.

## Wargi i zachowanie objętości

Uśmiech, wysunięcie warg, lejek i zawijanie warg nie mogą redukować objętości przez liniowe rozciąganie wierzchołków.

Minimalne kształty korekcyjne:

- `jawOpen × mouthSmile`;
- `jawOpen × mouthPucker`;
- `jawOpen × mouthFunnel`;
- `eyeBlink × eyeLookUp/Down`;
- `cheekSquint × eyeBlink`;
- `browDown × eyeSquint`;
- `mouthSmile × cheekSquint`.

## Kształty korekcyjne

Kształt korekcyjny (corrective shape) jest deformacją uruchamianą automatycznie, gdy kombinacja dwóch poprawnych ruchów daje błędny wynik.

Przykładowy sterownik:

`w_corrective = smoothstep(t0, t1, w_A * w_B)`

Punktem startowym może być `t0=0.15` i `t1=0.55`. Niższy `t0` uruchamia korekcję wcześniej; zbyt niski może zmieniać neutralne, subtelne ruchy. Wyższy `t1` opóźnia pełny wpływ i może pozostawić błąd w średnich zakresach.

## Policzki i bruzda nosowo-wargowa

Silny uśmiech powinien powodować uniesienie policzka i zmianę bruzdy nosowo-wargowej. `cheekSquint` powinien wpływać również na dolną powiekę i zewnętrzny kącik oka.

## Język

`tongueOut` zapewnia minimum interoperacyjności, ale rig wzorcowy powinien mieć sterowanie:

- podstawą języka;
- częścią środkową;
- czubkiem;
- opcjonalnym zagięciem bocznym.

Język podąża za żuchwą, zachowując niezależne ruchy artykulacyjne.

## Test pojedynczych kanałów

Każdy kanał należy sprawdzić przy:

`0.0, 0.25, 0.5, 0.75, 1.0`.

Fail występuje przy:

- skoku geometrii;
- utracie objętości;
- załamaniu normalnych;
- samoprzecięciu;
- niekontrolowanej asymetrii.

## Test kombinacji

Obowiązkowe pary i zestawy:

- smile + jaw open;
- pucker + jaw open;
- blink + eye look up/down;
- smile + cheek squint;
- brow down + squint;
- asymetryczny smile + jaw;
- mowa + mruganie + spojrzenie.

## Definition of Done

Rig twarzy jest zaliczony, gdy:

- 52 kanały ARKit są dostępne;
- żuchwa działa anatomicznie;
- oczy i powieki współpracują;
- domknięcie warg działa podczas mowy;
- kształty korekcyjne usuwają główne błędy kombinacji;
- FACS mapping jest udokumentowany;
- pojedyncze kanały i kombinacje przechodzą testy pośrednich wartości;
- rig nadaje się do face trackingu i lip-sync.