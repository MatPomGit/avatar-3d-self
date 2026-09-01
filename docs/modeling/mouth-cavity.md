# Jama ustna

Jama ustna jest częścią modelu odpowiedzialną za wnętrze widoczne podczas mowy, ziewania, uśmiechu i szerokiego otwarcia ust. W fotorealistycznym awatarze nie może być traktowana jako ciemna płaska powierzchnia za wargami.

## Elementy

Model powinien zawierać co najmniej:

- górny łuk zębowy,
- dolny łuk zębowy,
- dziąsła,
- język,
- podniebienie,
- dno jamy ustnej,
- wewnętrzną powierzchnię policzków i warg,
- ciemniejszą geometrię części tylnej jamy ustnej.

## Zęby

Zęby powinny być odwzorowane jako osobna geometria. Górne zęby poruszają się z czaszką, dolne z żuchwą.

Nie należy tworzyć idealnie białych, identycznych zębów. Naturalne uzębienie ma subtelne różnice jasności, przezierności szkliwa i kształtu.

### Prześwit między zębami

W neutralnym zwarciu nie powinno być widocznych sztucznych szczelin wynikających wyłącznie z uproszczonej geometrii. Jednocześnie zęby nie mogą przenikać przez siebie podczas `jawOpen` i ruchów bocznych żuchwy.

## Język

Język jest aktywnym elementem artykulacji. Nie wymaga pełnego modelu biomechanicznego, ale powinien umożliwiać kilka kontrolowanych pozycji.

Minimalne cele:

- pozycja neutralna,
- uniesienie czubka języka,
- wysunięcie czubka do przodu,
- uniesienie przedniej części,
- uniesienie tylnej części,
- cofnięcie języka,
- lekkie poszerzenie i zwężenie.

Dla polskiej mowy szczególnie istotne są ruchy języka dla grup `/t d n l r/`, głosek syczących i szeregu ciszącego.

## Zakres ruchu

Parametry nie powinny być definiowane jako arbitralne przesunięcia w jednostkach sceny. Sterowanie powinno być znormalizowane do zakresu 0-1, a rzeczywista deformacja wynikać z modelu konkretnej jamy ustnej.

Przykładowo `tongueTipUp = 0,25` oznacza subtelne uniesienie, `0,5` wyraźną artykulację, a `1,0` skrajne ustawienie używane głównie w testach. W normalnej mowie większość kanałów nie powinna stale dochodzić do 1,0.

## Materiał języka i dziąseł

Język i dziąsła są wilgotnymi tkankami. Powinny mieć niższą chropowatość niż sucha skóra, ale nie mogą wyglądać jak plastik.

Punkt startowy dla chropowatości:

- język: 0,25-0,40,
- dziąsła: 0,30-0,45,
- wewnętrzna warga: 0,20-0,35.

Zbyt niska chropowatość powoduje efekt lakierowanej powierzchni. Zbyt wysoka usuwa charakterystyczne wilgotne refleksy.

## Okluzja i ciemność wnętrza

Ciemność jamy ustnej powinna wynikać z geometrii, okluzji i materiałów, nie z jednolitej czarnej tekstury. Przy szerokim otwarciu nadal powinny być widoczne zróżnicowane powierzchnie języka, dziąseł i tylnej części jamy ustnej.

## Kolizje

W testach należy sprawdzić:

- język kontra zęby,
- język kontra podniebienie,
- dolne zęby kontra górne,
- wewnętrzna warga kontra zęby,
- policzek kontra łuki zębowe.

Przenikanie mniejsze niż około 0,5 mm może być niewidoczne w ruchu, ale nie powinno być akceptowane jako stały mechanizm działania. Widoczne przenikanie powyżej około 1 mm wymaga korekty.

## Testy artykulacyjne

Minimalny zestaw:

`/pa ba ma fa va ta da na la ra sa za sza cza ka ga/`

oraz samogłoski:

`/a e i o u y/`.

Testuj z przodu, z profilu i z kamery 3/4. Warto także czasowo wyłączyć skórę twarzy, aby obejrzeć samą pracę języka, zębów i żuchwy.

## Kryteria akceptacji

Jama ustna jest gotowa, gdy:

- nie widać pustej przestrzeni za wargami,
- zęby pozostają poprawnie związane z czaszką i żuchwą,
- język wspiera podstawowe klasy artykulacyjne,
- nie występują widoczne przenikania,
- materiały zachowują wilgotny, ale nie plastikowy wygląd,
- szerokie otwarcie ust pozostaje wiarygodne z wielu kątów.