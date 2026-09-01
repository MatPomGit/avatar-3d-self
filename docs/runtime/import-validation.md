# Walidacja importu do środowiska docelowego

Walidacja importu (import validation) sprawdza, czy artefakt pochodny po eksporcie zachowuje znaczenie danych wersji wzorcowej. Nie porównujemy wyłącznie tego, czy plik „otwiera się”. Sprawdzamy geometrię, skalę, deformację, materiały, animację i zachowanie w czasie.

## Scena referencyjna

Każdy adapter silnika powinien mieć małą scenę referencyjną zawierającą:

- neutralne światło frontalne;
- światło boczne;
- światło zza postaci;
- neutralne tło szare;
- kamerę twarzy;
- kamerę pełnej sylwetki;
- klip deformacji ciała;
- klip mimiki;
- klip mowy;
- test przełączania poziomów szczegółowości.

Ta sama scena logiczna powinna istnieć w Unreal, Unity i demonstratorze Web, nawet jeżeli implementacje oświetlenia nie są identyczne.

## 1. Skala i orientacja

Najpierw sprawdzamy wymiar postaci. Wysokość importowanego awatara powinna być zgodna z wersją wzorcową w granicy ±0,5%.

Następnie sprawdzamy osie:

- kierunek „przód”;
- oś pionową;
- orientację dłoni;
- kierunek zgięcia kolan i łokci;
- lokalne osie kości.

Jeżeli postać wygląda poprawnie w pozycji neutralnej, ale kości obracają się w nieprzewidywalny sposób, problemem mogą być lokalne układy osi, a nie sama animacja.

## 2. Geometria

Porównujemy:

- liczbę oczekiwanych siatek;
- obecność wszystkich części ciała;
- brak nowych szczelin;
- brak odwróconych powierzchni;
- poprawną kolejność przezroczystości tam, gdzie ma znaczenie;
- zgodność poziomów szczegółowości.

## 3. Wiązanie skóry z kośćmi

Klip testowy powinien zawierać co najmniej:

- odwiedzenie ramion;
- zgięcie łokci;
- skręt przedramienia;
- głęboki przysiad;
- uniesienie nogi;
- zgięcie nadgarstka;
- pełne zgięcie palców.

Widoczna penetracja lub załamanie geometrii w kluczowej pozie oznacza błąd krytyczny.

## 4. Twarz

Każdy kształt deformacyjny testujemy co najmniej przy wagach 0%, 25%, 50%, 75% i 100%.

Sprawdzamy:

- poprawną nazwę;
- kierunek deformacji;
- brak odwróconej skali;
- pełne domknięcie powiek;
- kontakt warg dla `/p b m/`;
- ruch żuchwy;
- niezależny ruch oczu;
- kształty korekcyjne.

Nie zakładamy, że wszystkie silniki używają tej samej skali wag. Przykładowo część API używa zakresu `0-1`, a interfejsy edytora mogą prezentować `0-100`. Adapter musi jawnie wykonywać przeliczenie.

## 5. Materiały

Dla każdej mapy potwierdzamy:

- przestrzeń barw;
- kanał;
- znak osi Y mapy normalnych;
- sposób pakowania kanałów;
- rozdzielczość;
- kompresję;
- obecność łańcucha mipmap.

Skórę porównujemy w świetle frontalnym i bocznym. Oko dodatkowo testujemy na refleksach rogówki, załamaniu światła i kontakcie powiek.

## 6. Włosy

Sprawdzamy:

- sylwetkę fryzury;
- gęstość;
- cienie;
- penetrację głowy i ubrań;
- ruch wtórny;
- zachowanie przy zmianie LOD.

Jeżeli silnik nie obsługuje źródłowego systemu włosów, adapter musi jawnie wskazywać zastosowaną reprezentację zastępczą.

## 7. Mowa

Klip testowy powinien zawierać co najmniej sekwencje `/pa ba ma fa va ta da ka ga sa za ra/` oraz kilka pełnych polskich zdań.

Sprawdzamy:

- zgodność początku audio i animacji;
- koartykulację;
- domknięcie warg;
- kontakt dolnej wargi z górnymi zębami dla `/f v/`;
- stabilność żuchwy;
- brak trzepotania krótkich fonemów.

## 8. Raport różnic

Każdy import tworzy raport zawierający:

- wersję wersji wzorcowej;
- profil eksportu;
- wersję silnika;
- format pliku;
- listę ostrzeżeń;
- listę utraconych funkcji;
- listę funkcji zastąpionych inną implementacją;
- wynik testów;
- sumy kontrolne plików wejściowych.

## Kryterium zaliczenia

Import jest zaliczony dopiero wtedy, gdy wszystkie testy krytyczne przechodzą w środowisku docelowym. Ostrzeżenie o celowo uproszczonym elemencie jest dopuszczalne tylko wtedy, gdy wynika z jawnego profilu LOD lub ograniczeń platformy.