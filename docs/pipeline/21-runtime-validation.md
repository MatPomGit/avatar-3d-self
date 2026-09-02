# 21. Walidacja czasu rzeczywistego

**Input:** zatwierdzona paczka eksportowa z etapu 20.  
**Editable output:** projekt testowy runtime i konfiguracja benchmarku.  
**Derived output:** raport akceptacyjny, pomiary wydajności i lista błędów.

## Cel etapu

Ostatni etap sprawdza, czy awatar działa poprawnie w docelowym środowisku, a nie tylko w Blenderze. Walidacja obejmuje jednocześnie geometrię, materiały, rig, mimikę, mowę, zachowanie i wydajność. Wynik musi być mierzony na jawnie określonym sprzęcie i konfiguracji renderingu.

## Przygotowanie

1. Utwórz czysty projekt testowy w docelowym silniku.
2. Zapisz wersję silnika, system operacyjny, GPU, CPU, RAM i sterownik GPU.
3. Ustal rozdzielczość renderingu, target FPS i profil jakości.
4. Zaimportuj dokładnie paczkę z etapu 20 bez ręcznych poprawek, które nie zostały zapisane w pipeline.
5. Zachowaj log importu i wszystkie ostrzeżenia.

## Test 1. Integralność importu

Sprawdź kolejno:

- liczbę meshów;
- skalę postaci;
- orientację osi;
- skeleton i root;
- liczbę kości;
- morph targets;
- materiały i tekstury;
- animacje;
- włosy/groom;
- okulary i przezroczystość soczewek.

Jeżeli importer wykonuje automatyczne zmiany, zapisz je jako część profilu runtime.

## Test 2. Geometria i LOD

Obejrzyj LOD0 z bliska i niższe poziomy z typowych odległości. Sprawdź:

1. silhouette popping;
2. znikanie palców, uszu lub okularów;
3. zmianę kształtu twarzy;
4. błędne normal maps po redukcji;
5. zachowanie UV i materiałów;
6. zgodność skeletonu pomiędzy LOD.

Zmiana LOD nie może zmieniać rozpoznawalnej tożsamości twarzy.

## Test 3. Materiały

Oceń awatara co najmniej w trzech warunkach oświetlenia:

- miękkie neutralne światło;
- mocne światło boczne;
- środowisko o wysokim kontraście.

Sprawdź skórę, SSS, roughness, oczy, cornea, włosy, brodę, ubrania i okulary. Materiał, który wygląda poprawnie tylko w jednym HDRI, nie jest wystarczająco zwalidowany.

## Test 4. Oczy

Oczy są krytycznym źródłem uncanny valley. Sprawdź:

- pozycję gałek ocznych;
- kierunek spojrzenia;
- highlight na rogówce;
- brak świecenia twardówki;
- reakcję powiek na ruch oka;
- szczelny blink;
- sakkady i mikroruchy.

Nienaturalne oczy należy traktować jako błąd wysokiego priorytetu nawet przy poprawnej geometrii reszty modelu.

## Test 5. Deformacja ciała

Uruchom zestaw póz z etapu skinningu i co najmniej jeden klip locomotion. Szukaj:

- zapadania barków;
- candy-wrapper twist;
- penetracji ubrań;
- sliding stóp;
- błędów dłoni;
- popping corrective shapes.

## Test 6. Twarz i emocje

Przetestuj:

1. neutral;
2. blink lewy/prawy i obustronny;
3. jaw open;
4. smile;
5. frown;
6. surprise;
7. anger;
8. fear;
9. disgust;
10. ekspresje mieszane;
11. asymetryczne blend shapes.

Oceniaj nie tylko zakres ruchu, ale zachowanie podobieństwa osoby przy ekspresji.

## Test 7. Mowa

Użyj reprezentatywnego fragmentu mowy wygenerowanego przez docelowy model Piper. Klip powinien zawierać różne samogłoski, spółgłoski wargowe i szybkie przejścia fonemiczne.

Sprawdź:

- synchronizację początku i końca wypowiedzi;
- jaw motion;
- bilabial closure dla /p/, /b/, /m/;
- koartykulację;
- brak przypadkowego drżenia warg;
- współpracę mowy z blink, gaze i head motion.

Nie akceptuj lip-sync sterowanego wyłącznie amplitudą audio jako docelowego rozwiązania.

## Test 8. Zachowanie bezczynne

Obserwuj postać przez co najmniej kilkadziesiąt sekund bez polecenia ruchu. Powinny występować subtelne, nieregularne:

- mrugnięcia;
- ruchy spojrzenia;
- oddychanie;
- mikroruchy głowy;
- zmiany ciężaru ciała.

Unikaj idealnie okresowych cykli, które szybko ujawniają mechaniczność animacji.

## Test 9. Wydajność

Mierz co najmniej:

- średni FPS;
- 1% low FPS lub równoważną metrykę frametime;
- CPU frame time;
- GPU frame time;
- pamięć GPU;
- RAM;
- liczbę draw calls;
- liczbę triangles dla aktywnego LOD.

Test wykonuj po rozgrzaniu sceny, nie tylko przez pierwsze kilka sekund.

## Test 10. Uncanny valley

Przeprowadź osobną inspekcję według [Uncanny valley](../validation/uncanny-valley.md). Problemy klasyfikuj według źródła: oczy, twarz, timing, skin, włosy, proporcje, mowa lub ruch ciała. Nie maskuj błędu stylizacją, jeżeli celem pozostaje fotorealizm.

## Kryteria błędu krytycznego

Do krytycznych błędów należą m.in.:

- niepoprawna skala lub skeleton;
- utrata wymaganych morph targets;
- widoczna utrata podobieństwa twarzy;
- poważne penetracje lub załamania deformacji;
- niesynchronizowana mowa;
- oczy powodujące silny efekt uncanny valley;
- niestabilny frametime uniemożliwiający działanie czasu rzeczywistego;
- crash lub błąd importu.

Błąd krytyczny blokuje finalne zatwierdzenie bez jawnego waivera.

## Raport

Raport runtime powinien zawierać:

1. hash paczki eksportowej;
2. wersję silnika;
3. sprzęt testowy;
4. ustawienia jakości;
5. wyniki wydajności;
6. wyniki testów geometrii, deformacji, twarzy i mowy;
7. listę ostrzeżeń;
8. waivery;
9. materiał porównawczy lub odnośniki do klipów walidacyjnych.

## DoD

Awatar przechodzi test importu, deformacji, twarzy, mowy i wydajności w zdefiniowanym środowisku. Raport pozwala odtworzyć warunki pomiaru i jednoznacznie wskazuje wszystkie zaakceptowane odstępstwa. Dopiero ten etap pozwala traktować konkretną wersję paczki jako zatwierdzony artefakt runtime.
