# Walidacja animacji twarzy

Walidacja animacji twarzy sprawdza jednocześnie geometrię deformacji, dynamikę ruchu i wiarygodność zachowania. Sam fakt, że kontroler lub kształt deformacyjny (blend shape) zmienia siatkę, nie oznacza poprawnej animacji. Twarz może być technicznie sterowalna, a jednocześnie sprawiać wrażenie martwej, gumowej albo mechanicznej.

W Avatar Studio walidacja jest wykonywana po zbudowaniu układu sterowania twarzą, po integracji mowy oraz ponownie po imporcie do środowiska czasu rzeczywistego.

## Warstwy walidacji

Test dzielimy na pięć warstw:

1. poprawność pojedynczych kanałów;
2. poprawność kombinacji kanałów;
3. dynamika i czas ruchu;
4. zachowanie podczas mowy i emocji;
5. zgodność w docelowym rendererze.

Błąd na wcześniejszej warstwie należy naprawić przed próbą kompensowania go na późniejszej.

## Monotoniczność kanału

**Monotoniczność deformacji (deformation monotonicity)** oznacza, że zwiększanie wartości sterownika powinno konsekwentnie zwiększać znaczenie danego ruchu. Nie wymaga liniowego przesunięcia wierzchołków, ale zabrania sytuacji, w której np. uśmiech przy `0.75` jest wizualnie słabszy niż przy `0.50`.

Każdy kanał interoperacyjny testuj przy:

```text
0.00
0.25
0.50
0.75
1.00
```

Kanał otrzymuje `fail`, jeśli pojawia się:

- skok geometrii;
- odwrócenie kierunku ruchu;
- nagła utrata objętości;
- samoprzecięcie;
- niezamierzona deformacja odległego regionu;
- zmiana strony lewa/prawa;
- załamanie powierzchni widoczne dopiero przy wartościach pośrednich.

## Test 52 kanałów ARKit

Warstwa kompatybilności ARKit używa zakresu `0..1`. Każdy z 52 kanałów musi mieć test pojedynczy oraz informację, czy mapuje się na:

- kształt deformacyjny;
- kość lub transformację;
- kilka kontrolerów wewnętrznych;
- procedurę korekcyjną.

Dla kanałów lewych i prawych test wykonuj osobno. Zgodność nazw nie jest wystarczająca. `mouthSmileLeft` musi faktycznie sterować lewą stroną twarzy, a `eyeLookInLeft` poprawnym kierunkiem lewego oka.

## Kalibracja sygnału wejściowego

Sygnał z trackingu może wymagać mapowania:

`w_avatar = f(w_tracking)`

Funkcja `f` może ograniczać lub wzmacniać określony zakres. Przykładowo wartość `0.8` z urządzenia nie musi oznaczać, że awatar powinien natychmiast użyć 80% maksymalnego dobrowolnego uśmiechu.

Walidacja powinna sprawdzić przynajmniej:

- `0.0` jako rzeczywisty neutral;
- zakres rozmowy około `0.1-0.55`;
- mocne ekspresje około `0.6-0.8`;
- skrajne wartości `0.8-1.0` jako zakres kalibracyjny, a nie typowy stan rozmowy.

Zbyt agresywna funkcja mapująca prowadzi do przerysowanej mimiki i efektu doliny niesamowitości. Zbyt słaba daje twarz bez wyrazu.

## Żuchwa

`jawOpen` testuj geometrycznie i dynamicznie. Wartość `1.0` powinna odpowiadać zatwierdzonemu maksymalnemu otwarciu konkretnej osoby, z punktem startowym około 30-35 mm rozwarcia między siekaczami i kątem około 25-30° dla typowego dorosłego modelu.

Testy:

- `jawOpen` 0, 0.25, 0.5, 0.75, 1;
- `jawForward`;
- `jawLeft` i `jawRight`;
- `jawOpen × mouthSmile`;
- `jawOpen × mouthPucker`;
- `jawOpen × mouthFunnel`.

`fail` występuje, gdy żuchwa obraca się jak prosty techniczny zawias, dolna warga odłącza się od ruchu, zęby przenikają przez tkanki albo broda traci objętość.

## Domknięcie warg

**Domknięcie warg (lip seal)** jest zdolnością górnej i dolnej wargi do utrzymywania rzeczywistego kontaktu przy niewielkim otwarciu żuchwy. Jest niezbędne dla `/p b m/`.

Baseline projektu:

- pełne działanie do `jawOpen = 0.08`;
- stopniowe wygaszenie;
- około `jawOpen = 0.22` wpływ powinien być bliski zeru.

Przetestuj także `mouthClose`, `mouthPress`, `mouthPucker` oraz mowę. Błąd polega m.in. na zasysaniu warg do wnętrza, ślizganiu się jednej wargi po drugiej albo pozostawaniu szczeliny przy fonemach dwuwargowych.

## Mruganie

Mrugnięcie nie jest zwykłym ruchem suwaka od 0 do 1. Jego wiarygodność zależy od geometrii i czasu.

Baseline naturalnego mrugnięcia:

| Parametr | Punkt odniesienia |
| --- | ---: |
| całkowity czas | 170 ms |
| typowy zakres | 140-240 ms |
| zamykanie | 55 ms |
| kontakt | 20 ms |
| otwieranie | 95 ms |
| typowa niewielka asymetria L/R | około 8 ms |

Testuj:

- lewy blink;
- prawy blink;
- blink obustronny;
- blink podczas spojrzenia w górę;
- blink podczas spojrzenia w dół;
- blink podczas `cheekSquint`;
- blink w trakcie mowy.

Pełne zamknięcie nie może pozostawiać szczeliny przez rogówkę ani powodować penetracji gałki ocznej. Dolna powieka powinna uczestniczyć w ruchu, ale zwykle mniej niż górna.

## Śledzenie powiek za ruchem oka

**Śledzenie powiek za ruchem oka (eyelid follow)** oznacza subtelne przesunięcie powiek zgodne z pionową rotacją gałki ocznej. Bez niego oko wygląda jak kula obracająca się niezależnie pod nieruchomą maską skóry.

Punkty startowe:

- spojrzenie w górę: wpływ około `0.30-0.35`;
- spojrzenie w dół: około `0.40-0.45`.

Zbyt duża wartość wygląda jak wymuszone unoszenie lub opuszczanie powiek. Zbyt mała daje martwy, mechaniczny wzrok.

## Sakkady

**Sakkada (saccade)** jest szybkim ruchem oka pomiędzy punktami fiksacji. W projekcie czas sakkady jest modelowany orientacyjnie przez:

`T_saccade_ms = clamp(25 + 2.5 × A, 30, 90)`

gdzie `A` jest amplitudą w stopniach.

Przykłady:

- 5° → około 38 ms;
- 10° → około 50 ms;
- 20° → około 75 ms.

W rozmowie większość czytelnych zmian spojrzenia mieści się około 2-12°. Większe ruchy 12-20° powinny występować rzadziej, a przy zmianie celu przekraczającej około 25-30° zwykle powinien dołączyć ruch głowy.

## Mikrosakkady

**Mikrosakkada (microsaccade)** jest bardzo małym, mimowolnym ruchem oka występującym podczas fiksacji. Punkt startowy projektu:

- amplituda około 0.1-0.6°;
- częstotliwość około 0.4-1.2 Hz.

Zbyt duża amplituda powoduje nerwowe drżenie wzroku. Całkowity brak mikroruchu podczas długiej fiksacji może sprawiać wrażenie sztuczności.

## Fiksacje

Dla obiektów w scenie typowa fiksacja może trwać około 220-650 ms. W rozmowie patrzenie na twarz rozmówcy może utrzymywać się dłużej, orientacyjnie 0.7-2.5 s, z okresowym odwracaniem spojrzenia około 0.2-1.1 s.

Nie należy generować tych wartości z dokładnym okresem. Zakres służy do kontroli statystycznej, a nie do zaprogramowania metronomu.

## Kształty korekcyjne

**Kształt korekcyjny (corrective shape)** naprawia deformację, która jest poprawna dla pojedynczych kanałów, ale błędna dla ich kombinacji.

Priorytetowe kombinacje:

- `jawOpen × mouthSmile`;
- `jawOpen × mouthPucker`;
- `jawOpen × mouthFunnel`;
- `eyeBlink × eyeLookUp/Down`;
- `cheekSquint × eyeBlink`;
- `browDown × eyeSquint`;
- `mouthSmile × cheekSquint`.

Dla każdego corrective zapisz:

- warunek aktywacji;
- zakres wejściowy;
- sposób obliczania wagi;
- obraz lub klip przed naprawą;
- wynik po naprawie;
- test regresyjny.

## FACS

Walidacja FACS nie polega na sprawdzeniu nazw. **Jednostka działania mięśniowego (Action Unit, AU)** opisuje obserwowalny ruch określonego regionu twarzy.

Dla najważniejszych ruchów sprawdź zgodność co najmniej z:

- AU1;
- AU2;
- AU4;
- AU6;
- AU7;
- AU9;
- AU10;
- AU12;
- AU15;
- AU17;
- AU18;
- AU25;
- AU26.

Sprawdź również kombinacje. Przykładowo naturalny silny uśmiech nie powinien poruszać wyłącznie kącików ust. Zwykle pojawia się udział policzków, bruzd nosowo-wargowych i często AU6.

## Naturalna asymetria

Idealna symetria nie jest celem. W materiale referencyjnym mogą istnieć trwałe różnice między lewą i prawą stroną. Walidacja powinna rozróżniać:

- asymetrię osoby referencyjnej;
- asymetrię chwilowej ekspresji;
- błąd modelu lub rigu.

Nie naprawiaj asymetrii tylko dlatego, że lewa i prawa strona nie dają identycznych wartości geometrycznych.

## Dynamika emocji

Dla ekspresji używamy znormalizowanego natężenia `0..1`. Typowa rozmowa powinna najczęściej pracować około `0.1-0.55`. Wartości `0.8-1.0` są zarezerwowane dla mocnych szczytów ekspresji.

Punkt startowy dynamiki:

- czas narastania około 250 ms;
- faza maksymalnego nasilenia około 700 ms;
- czas wygaszania około 450 ms;
- różnica stron dla wielu naturalnych ruchów około 5-12%.

Te wartości nie są stałym presetem każdej emocji. Służą jako diagnostyczna baza do wykrywania natychmiastowego „włączania” i „wyłączania” ekspresji.

## Test koartykulacji

**Koartykulacja (coarticulation)** oznacza czasowe nakładanie się ruchów sąsiadujących fonemów. Testuj minimum:

```text
/pa ba ma fa va ta da ka ga sa za ra/
```

oraz naturalne zdania po polsku.

Baseline:

- wizualne wyprzedzenie artykulacji: około 60 ms, zakres 40-100 ms;
- narastanie przejścia: około 50-80 ms;
- wygaszanie: około 80-120 ms.

`fail` występuje, gdy wizemy skaczą pomiędzy dyskretnymi kształtami, ruch ust jest stale spóźniony względem dźwięku albo każdy fonem osiąga pełne `1.0` bez uwzględniania kontekstu.

## Test fonemów kontaktowych

Dla `/p b m/` sprawdź pełny kontakt warg. Dla `/f v/` dolna warga powinna zbliżać się do górnych zębów. Dla polskich spółgłosek językowych widoczna geometria języka nie musi przesadnie wychodzić na pierwszy plan, ale układ jamy ustnej powinien być wiarygodny przy otwartych ustach.

## Mowa nie może animować wyłącznie ust

Podczas wypowiedzi sprawdź jednocześnie:

- żuchwę;
- policzki;
- subtelne ruchy brwi;
- mruganie;
- ruch oczu;
- mikroruchy głowy;
- gesty, jeśli kamera obejmuje ciało.

Twarz z poprawnym lip-sync, ale zamrożonymi oczami i policzkami nadal otrzymuje `fail` w teście wiarygodności behawioralnej.

## Test 60 s

Nagraj co najmniej 60 s zbliżenia neutralnego stanu bezczynności i swobodnej rozmowy.

Automatycznie raportuj:

- liczbę mrugnięć;
- średni, minimalny i maksymalny odstęp między mrugnięciami;
- liczbę sakkad;
- rozkład amplitud sakkad;
- czas fiksacji;
- zakres ruchu głowy;
- średnie i maksymalne wartości kanałów twarzy.

Punkt startowy częstości mrugania to około 12/min, z szerokim naturalnym zakresem około 6-20/min. Minimalny odstęp około 1.2 s może być użyty jako ostrzeżenie przed mechanicznie częstymi powtórzeniami, ale nie jako biologiczny zakaz.

## Test ekspresji mieszanych

Przynajmniej następujące kombinacje powinny zostać ocenione:

- uśmiech + mowa;
- smutek + mowa;
- zaskoczenie + spojrzenie boczne;
- squint + uśmiech;
- browDown + eyeSquint;
- uśmiech asymetryczny;
- szybkie przejście między dwoma stanami emocjonalnymi.

Test ma wykryć konflikty pomiędzy warstwami, nie tylko poprawność pojedynczej pozy.

## Test z okularami

Ponieważ okulary są istotnym elementem twarzy, test wykonuj także z finalnym modelem oprawek. Sprawdź:

- kolizje brwi z oprawą;
- penetrację rzęs przez soczewki;
- kontakt oprawek z policzkiem podczas silnego uśmiechu;
- nieprawidłowe odbicia zasłaniające oczy;
- stabilność okularów przy ruchu głowy.

## Macierz walidacyjna

Każdy test zapisuj jako rekord:

```yaml
test_id: FAC_blink_down_001
subsystem: eyelids
inputs:
  eyeBlinkLeft: 1.0
  eyeBlinkRight: 1.0
  eyeLookDownLeft: 0.6
  eyeLookDownRight: 0.6
result: pass
severity: 0
artifact: reports/facial/FAC_blink_down_001.mp4
notes: "full closure, no cornea penetration"
```

Statusy:

- `pass`: brak istotnego problemu;
- `warning`: problem niewidoczny w typowym użyciu lub dotyczący skrajnego zakresu;
- `fail`: widoczny błąd w zakresie używanym przez środowisko czasu rzeczywistego.

## Istotność błędu

Do triage stosuj skalę 1-5:

1. kosmetyczny, widoczny dopiero podczas inspekcji;
2. zauważalny, ale niewpływający wyraźnie na wiarygodność;
3. regularnie widoczny i obniżający jakość;
4. poważny błąd powodujący efekt sztuczności;
5. krytyczny, np. penetracja oka, rozrywanie ust, nieprawidłowa strona kanału lub utrata synchronizacji mowy.

Błędy 4-5 blokują zatwierdzenie. Błędy 3 wymagają jawnej decyzji przed wydaniem. Błędy 1-2 mogą zostać odłożone tylko z zapisanym uzasadnieniem.

## Test regresyjny

Po każdej zmianie topologii, skinningu, kształtu deformacyjnego, mapowania ARKit, materiału oka lub procedury koartykulacji ponownie uruchom odpowiedni zestaw testów. Nie wystarczy sprawdzić jedynie naprawiony kanał, jeśli zmiana wpływa na wspólną geometrię.

Minimalna regresja twarzy:

```text
neutral
blink
look up/down/left/right
jaw open
lip seal
smile L/R
frown L/R
pucker
funnel
brows
cheek squint
nose sneer
speech corpus
mixed expression clip
```

## Walidacja w rendererze docelowym

Model zatwierdzony w Blenderze może wyglądać inaczej po imporcie do Unreal Engine, Unity lub Web. Dlatego końcowy test powtarza się w środowisku docelowym z tym samym klipem wejściowym.

Porównaj:

- skalę wag morph targets;
- kolejność aktualizacji kości i kształtów;
- interpolację krzywych;
- ruch oczu i powiek;
- materiały rogówki i skóry;
- zachowanie włosów i okularów;
- czas klatki i pominięte aktualizacje animacji.

## Definition of Done

Animacja twarzy jest zatwierdzona, jeśli:

- 52 kanały ARKit przechodzą testy 0/0.25/0.50/0.75/1.00;
- wszystkie kanały są monotoniczne semantycznie;
- żuchwa, usta, policzki, brwi, nos i powieki nie tworzą istotnych penetracji;
- blink ma prawidłową geometrię i naturalny zakres czasowy;
- spojrzenie zawiera sakkady, fiksacje, mikroruchy i śledzenie powiek;
- kluczowe AU FACS są anatomicznie wiarygodne;
- naturalna asymetria została zachowana;
- kształty korekcyjne usuwają błędy najważniejszych kombinacji;
- mowa ma poprawne kontakty warg i koartykulację;
- test 60 s nie wykazuje mechanicznej periodyczności;
- ekspresje mieszane nie powodują konfliktów warstw;
- finalne okulary nie kolidują z twarzą;
- ten sam zestaw testów przechodzi po imporcie do środowiska docelowego;
- dla każdego `warning` i `fail` istnieje zapisany raport i decyzja.
