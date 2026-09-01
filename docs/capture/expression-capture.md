# Rejestracja ekspresji twarzy

Rejestracja ekspresji twarzy (expression capture) jest kontrolowaną sesją referencyjną służącą do budowy, kalibracji i walidacji układu sterowania twarzą (facial rig). Nie zastępuje neutralnej fotogrametrii. Jej celem nie jest rekonstrukcja całej głowy z każdej miny, lecz zebranie wiarygodnych przykładów tego, jak konkretna twarz zmienia kształt podczas ruchu.

W Avatar Studio materiał ten służy do:

- projektowania kształtów deformacyjnych (blend shapes);
- budowy kształtów korekcyjnych (corrective shapes);
- sprawdzania relacji ARKit i FACS z rzeczywistą anatomią osoby;
- kalibracji maksymalnych i pośrednich zakresów ruchu;
- oceny naturalnej asymetrii;
- kontroli mrugania, spojrzenia i ruchów żuchwy;
- przygotowania animacji mowy i koartykulacji.

## Dlaczego neutralna twarz jest obowiązkowa

**Poza neutralna twarzy (neutral facial pose)** jest stanem odniesienia, względem którego mierzymy wszystkie późniejsze deformacje. Jeśli neutral zmienia się pomiędzy ujęciami, różnica może zostać błędnie przypisana konkretnej ekspresji.

Neutral oznacza:

- brak świadomego uśmiechu i marszczenia brwi;
- naturalnie rozluźnione powieki;
- żuchwę w pozycji spoczynkowej;
- usta zamknięte bez zaciskania;
- brak unoszenia brody;
- wzrok skierowany do ustalonego punktu.

Rejestruj neutral na początku każdej grupy ekspresji oraz po każdej dłuższej przerwie. Przy sesji trwającej kilkadziesiąt minut warto wykonać dodatkowy neutral co około 5-10 minut, aby wykryć dryf pozy lub zmęczenie mięśni.

## Stabilność kamery i oświetlenia

Do porównania ruchu twarzy potrzebny jest stały układ obserwacji. Zmiana ogniskowej, odległości lub pozycji aparatu może wyglądać jak zmiana proporcji twarzy.

Wymagania:

1. kamera na stabilnym statywie;
2. stała ogniskowa;
3. stała ostrość albo ręcznie kontrolowany autofokus bez przeogniskowania w trakcie klipu;
4. zablokowana ekspozycja;
5. stały balans bieli;
6. brak trybów upiększania, portretowych i automatycznego modelowania twarzy;
7. miękkie, stabilne światło pozwalające widzieć fałdy skóry bez głębokich cieni zasłaniających anatomię.

Dla głównej kamery twarz powinna zajmować większość kadru, ale z pozostawieniem marginesu na pełne otwarcie ust, uniesienie brwi i niewielki ruch głowy.

## Widoki

Widok frontalny jest obowiązkowy, ale nie wystarcza do ruchów mających istotny komponent głębokości. Dla ważnych ekspresji wykonaj dodatkowo ujęcie około 45° z lewej lub prawej strony.

Widok 3/4 szczególnie pomaga ocenić:

- projekcję policzka;
- bruzdę nosowo-wargową;
- protruzję i zwężanie ust;
- wysunięcie żuchwy;
- ruch brody;
- unoszenie skrzydełka nosa;
- zmianę objętości warg.

Nie zmieniaj kąta w obrębie jednej serii natężenia. Jeżeli potrzebny jest drugi widok, powtórz serię z nowym, udokumentowanym ustawieniem kamery.

## Natężenie ekspresji

**Natężenie ekspresji (expression intensity)** opisuje, jak daleko ruch odchodzi od pozy neutralnej. Nie jest to bezpośredni pomiar siły mięśniowej. W materiale referencyjnym używamy znormalizowanej skali `0..1`, ponieważ później odpowiada ona wygodnie zakresowi wejściowemu ARKit i wewnętrznych sterowników.

Przykładowa interpretacja:

| Wartość | Znaczenie | Zastosowanie |
| ---: | --- | --- |
| `0.00` | neutral | pozycja odniesienia |
| `0.25` | subtelna ekspresja | mikroekspresje, rozmowa |
| `0.50` | średnia | typowa czytelna mimika |
| `0.75` | silna | wyraźna emocja lub artykulacja |
| `1.00` | maksymalna dobrowolna | kalibracja skrajnego zakresu |

Nie należy zakładać, że połowa geometrycznego przesunięcia wierzchołków odpowiada ekspresji `0.5`. Skala opisuje natężenie semantyczne, a późniejsze mapowanie może być nieliniowe.

Zbyt duży udział ujęć `1.0` prowadzi do rigu zoptymalizowanego pod grymasy zamiast naturalnej rozmowy. Zbyt mały zakres nie pokazuje natomiast pełnej anatomii ruchu i utrudnia budowę poprawnych kształtów korekcyjnych.

## Kanoniczny zestaw ruchów

### Żuchwa i usta

Zarejestruj:

- neutral;
- `jawOpen`;
- `jawForward`;
- `jawLeft` i `jawRight`;
- zamknięcie warg bez zaciskania;
- dociśnięcie warg;
- `mouthPucker`;
- `mouthFunnel`;
- `mouthSmileLeft` i `mouthSmileRight`;
- uśmiech obustronny;
- `mouthFrownLeft` i `mouthFrownRight`;
- opuszczenie dolnej wargi;
- uniesienie górnej wargi;
- rozciągnięcie kącików ust;
- zawinięcie górnej i dolnej wargi.

Dla `jawOpen` wykonaj serię stopniowaną. Maksimum nie powinno wymagać bólu ani nienaturalnego forsowania stawu skroniowo-żuchwowego.

### Policzki i nos

Zarejestruj:

- `cheekPuff`;
- `cheekSquintLeft` i `cheekSquintRight`;
- `noseSneerLeft` i `noseSneerRight`;
- silny naturalny uśmiech pokazujący współpracę policzka i dolnej powieki.

### Brwi i czoło

Zarejestruj:

- `browInnerUp`;
- `browOuterUpLeft` i `browOuterUpRight`;
- `browDownLeft` i `browDownRight`;
- uniesienie obu brwi;
- marszczenie brwi z naturalnym napięciem okolicy nasady nosa.

### Powieki

Zarejestruj:

- naturalne mrugnięcie obustronne;
- powolne kontrolowane zamknięcie powiek;
- `eyeBlinkLeft` i `eyeBlinkRight`, jeśli osoba potrafi wykonać je bez dużych ruchów reszty twarzy;
- `eyeSquintLeft/Right`;
- `eyeWideLeft/Right`.

Nie należy wymuszać idealnego mrugnięcia jednego oka, jeśli powoduje ono nienaturalne napięcie całej połowy twarzy. Taki materiał nadal może być użyteczny, ale musi zostać oznaczony jako ruch współzależny.

## Rejestracja spojrzenia

**Fiksacja wzroku (gaze fixation)** jest okresem utrzymywania wzroku na konkretnym celu. Do kalibracji kierunku oczu użyj fizycznych lub ekranowych punktów referencyjnych, zamiast polecenia „patrz trochę w lewo”.

Minimalny zestaw:

- środek;
- lewo i prawo około 10°;
- lewo i prawo około 20°;
- góra około 10° i 20°;
- dół około 10° i 20°;
- cztery kierunki ukośne.

Dla każdego punktu utrzymaj fiksację przez około 0,5-1 s. Nie oceniaj zakresu oka z pojedynczej klatki złapanej podczas sakkady.

**Sakkada (saccade)** jest szybkim ruchem oka pomiędzy punktami fiksacji. Dodatkowo nagraj kilka sekwencji przełączania wzroku między dwoma punktami oddalonymi o około 5°, 10° i 20°. Materiał ten służy później do oceny czasu ruchu oraz śledzenia powiek za ruchem oka (eyelid follow).

## Rejestracja naturalnego mrugania

Kontrolowane zamknięcie powiek jest potrzebne do geometrii, ale nie pokazuje naturalnego czasu mrugnięcia. Nagraj również co najmniej 60 s neutralnego patrzenia i swobodnej rozmowy.

Punkt odniesienia projektu dla pojedynczego naturalnego mrugnięcia:

- całkowity czas około 170 ms;
- typowy zakres około 140-240 ms;
- faza zamykania około 55 ms;
- krótki kontakt około 20 ms;
- otwieranie około 95 ms.

Nie należy instruować osoby, aby mrugała co określony czas. Celem jest zebranie naturalnej zmienności.

## FACS

**System Kodowania Ruchów Twarzy (Facial Action Coding System, FACS)** opisuje obserwowalne ruchy twarzy za pomocą jednostek działania mięśniowego (Action Units, AU). Materiał ekspresyjny powinien umożliwiać późniejsze sprawdzenie kluczowych AU, ale nie trzeba wymuszać czystej izolacji każdej jednostki u osoby, która nie jest przeszkolonym koderem FACS.

Szczególnie wartościowe są:

- AU1, wewnętrzne uniesienie brwi;
- AU2, zewnętrzne uniesienie brwi;
- AU4, opuszczenie brwi;
- AU6, uniesienie policzka;
- AU7, napięcie powiek;
- AU9, zmarszczenie nosa;
- AU10, uniesienie górnej wargi;
- AU12, uniesienie kącika ust;
- AU15, opuszczenie kącika ust;
- AU17, uniesienie brody;
- AU18, wysunięcie warg;
- AU25, rozchylenie warg;
- AU26, opuszczenie żuchwy.

Jeśli ruch ARKit i AU nie są relacją 1:1, w manifeście zapisujemy oba opisy zamiast sztucznie wymuszać jeden identyfikator.

## Naturalne emocje

Po ruchach kontrolowanych zarejestruj naturalne ekspresje:

- radość;
- smutek;
- złość;
- strach;
- zaskoczenie;
- obrzydzenie;
- co najmniej kilka ekspresji mieszanych.

Nie używaj ich jako prostych presetów `emocja = jeden kształt`. Są materiałem do oceny kombinacji AU, asymetrii, kolejności aktywacji regionów twarzy i dynamiki przejść.

Dla naturalnych emocji preferuj krótkie przejście:

```text
neutral → narastanie → maksimum → wygaszanie → neutral
```

Zachowaj kilka sekund neutralu przed i po ruchu.

## Mowa i koartykulacja

**Koartykulacja (coarticulation)** oznacza nakładanie się ruchów artykulacyjnych sąsiadujących głosek. Usta zaczynają przygotowywać się do kolejnego fonemu, zanim poprzedni całkowicie się zakończy. Dlatego referencja dla mowy nie może składać się wyłącznie z nieruchomych „kształtów wizemów”.

Nagraj co najmniej:

- `pa ba ma` dla pełnego domknięcia warg;
- `fa wa` dla kontaktu dolnej wargi z górnymi zębami;
- `ta da na la`;
- `ka ga ha`;
- `sa za ca dza`;
- `sza ża cza dża`;
- `sia zia cia dzia nia`;
- ciąg samogłosek `a e i y o u`;
- kilka naturalnych zdań w wolnym, średnim i szybkim tempie.

Do animacji bazowej projektu przyjmujemy wizualne wyprzedzenie ruchu ust około 60 ms, typowo 40-100 ms, oraz zakresy koartykulacji około 50-80 ms dla narastania i 80-120 ms dla wygaszania. Są to punkty startowe do późniejszej kalibracji, a nie parametry, które osoba ma świadomie odtwarzać podczas nagrania.

## Ruch głowy

W serii kalibracyjnej głowa powinna pozostać możliwie stabilna. Dla naturalnej mowy nagraj jednak osobny materiał z dozwolonymi mikroruchami głowy. Rozdzielenie tych dwóch typów nagrań umożliwia później odróżnienie deformacji twarzy od zachowania całej głowy.

## Manifest

Każdy klip lub seria zdjęć powinny mieć metadane:

```yaml
expression_id: mouth_smile_left
capture_type: controlled_expression
view: frontal
side: left
intensity_target: 0.50
arkit_channels:
  - mouthSmileLeft
facs_au:
  - AU12
neutral_reference: neutral_004
camera_profile: face_cam_v1
lighting_profile: soft_neutral_v1
notes: "natural asymmetry retained"
```

Dla klipu mowy dodaj tekst, język, tempo i identyfikator nagrania audio.

## Nazewnictwo plików

Nazwy mają być deterministyczne. Przykład:

```text
EXP_mouthSmileLeft_I025_front_take01.mp4
EXP_mouthSmileLeft_I050_front_take01.mp4
EXP_mouthSmileLeft_I075_front_take01.mp4
EXP_mouthSmileLeft_I100_front_take01.mp4
```

Nie używaj nazw `smile_good`, `smile2` ani `final`.

## Windows

Przykładowa struktura prywatnego workspace:

```text
D:\AvatarStudio\projects\self-avatar\capture\expressions\
```

Po sesji oblicz SHA-256 manifestu i sprawdź, czy nagrania są czytelne w pełnej rozdzielczości.

## Linux

Przykład:

```text
/home/<user>/AvatarStudio/projects/self-avatar/capture/expressions/
```

Używaj tej samej konwencji identyfikatorów i manifestu co na Windows.

## Kontrola jakości

Serię powtórz, jeśli:

- ostrość odpływa z oczu lub ust;
- automatyczna ekspozycja zmienia jasność podczas ruchu;
- ruch głowy zasłania deformację, która miała być izolowana;
- włosy lub okulary zakrywają krytyczny region twarzy;
- osoba nie wraca do neutralu;
- maksymalny ruch jest wymuszony bólem lub widocznym dyskomfortem;
- kluczowy ruch nie ma widoku pokazującego jego komponent głębokości.

## Definition of Done

Sesja ekspresji jest zaliczona, jeśli:

- istnieje zatwierdzony neutral i neutralne odniesienia między seriami;
- kluczowe ruchy mają co najmniej trzy poziomy natężenia, a najważniejsze cztery poziomy `0.25/0.50/0.75/1.00`;
- zarejestrowano oczy, powieki, żuchwę, usta, policzki, nos i brwi;
- istnieje materiał do kalibracji spojrzenia;
- istnieje co najmniej 60 s naturalnego mrugania i zachowania twarzy;
- zarejestrowano ruchy FACS/ARKit potrzebne do rigu;
- zarejestrowano naturalne emocje i kombinacje;
- istnieje materiał mowy pokazujący koartykulację;
- każdy artefakt jest powiązany z manifestem, profilem kamery i neutralem;
- materiał prywatny pozostaje poza publicznym repozytorium.
