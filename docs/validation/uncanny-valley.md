# Audyt efektu doliny niesamowitości

**Efekt doliny niesamowitości (uncanny valley)** opisuje sytuację, w której postać bardzo przypomina człowieka, ale niewielkie niespójności wyglądu lub zachowania powodują silne wrażenie sztuczności. W Avatar Studio nie traktujemy go jako pojedynczej metryki. Jest to klasa problemów wynikających z niespójności między geometrią, materiałami, ruchem, spojrzeniem i mową.

## Zasada niespójności

Im bardziej realistyczny jest jeden podsystem, tym bardziej widoczny staje się błąd innego. Fotorealistyczna skóra połączona z mechanicznym mruganiem może wyglądać gorzej niż prostsza stylizacja.

Dlatego audyt wykonuj warstwowo:

1. nieruchomy model,
2. oczy i mruganie,
3. mimika,
4. mowa,
5. gesty i ciało,
6. pełne środowisko czasu rzeczywistego.

## Oczy i spojrzenie

### Zbieżność oczu

**Zbieżność oczu (ocular convergence)** to skierowanie obu osi spojrzenia na ten sam punkt. Przy obiekcie bliskim oczy obracają się lekko do wewnątrz, przy dalekim są bardziej równoległe.

Błędy:

- brak zbieżności daje wrażenie patrzenia „przez” rozmówcę,
- zbyt duża zbieżność daje efekt zeza,
- identyczny ruch obu oczu bez mikroasymetrii wygląda mechanicznie.

### Twardówka

Zbyt duża ilość widocznej twardówki nad lub pod tęczówką może dawać wrażenie strachu albo „martwego oka”. Waliduj ją względem referencji w neutralnym spojrzeniu.

### Mikrosakkady

Mikrosakkady powinny być subtelne. Zakres 0,1-0,6° jest punktem startowym. Ruchy większe niż około 1° wykonywane często zaczynają wyglądać jak nerwowe skakanie wzroku.

## Mruganie

Neutralna częstość około 12 mrugnięć/min może służyć jako punkt startowy, ale akceptowalny zakres jest szerszy, około 6-20/min zależnie od sytuacji.

Objawy błędu:

- idealnie stały odstęp między mrugnięciami wygląda proceduralnie,
- pełna symetria obu powiek wygląda sztucznie,
- za szybkie mrugnięcie może wyglądać jak błąd animacji,
- za wolne daje efekt ciężkich lub sennych powiek.

Dla pojedynczego pełnego mrugnięcia używamy punktu startowego około 170 ms, z typowym zakresem 140-240 ms.

## Twarz

### Symetria

Idealna symetria ekspresji jest częstym źródłem sztuczności. Dla wielu ekspresji stosuj niewielką różnicę amplitudy lub czasu między stronami, np. 5-12%.

### Policzki

Uśmiech nie może ograniczać się do kącików ust. Powinien wpływać na policzek, dolną powiekę i bruzdę nosowo-wargową.

### Żuchwa

Żuchwa nie jest technicznym zawiasem. Przy otwieraniu ust zmieniają się policzki, dolna warga, okolica podbródka i szyja. Jeśli obraca się tylko dolny blok twarzy, rezultat wygląda mechanicznie.

## Mowa

Najczęstsze problemy:

- przeskakiwanie między wizemami,
- brak koartykulacji,
- zbyt szerokie otwieranie ust,
- brak pełnego kontaktu dla `/p b m/`,
- brak różnicy między samogłoskami,
- nieruchome policzki podczas mowy,
- język niezgodny z artykulacją,
- animacja ust uruchamiana wyłącznie amplitudą audio.

### Nadmierna amplituda

Jeżeli większość kanałów mowy regularnie osiąga 1,0, twarz wygląda przesadnie. W normalnej rozmowie duża część ruchów powinna pozostawać w zakresie około 0,2-0,7, a pełne wartości być zarezerwowane dla wyraźnych kontaktów lub akcentowanych ruchów.

## Materiały

### Skóra

Sprawdź:

- jednolitą chropowatość,
- zbyt mocne pory,
- nadmierne rozpraszanie podpowierzchniowe,
- brak lokalnych różnic koloru,
- zbyt błyszczące czoło i policzki.

### Oczy

Sprawdź:

- czysto białą twardówkę,
- brak warstwy łzowej,
- płaską tęczówkę,
- zbyt mocne lub zbyt słabe refleksy rogówki.

### Zęby

Idealnie białe, identyczne zęby mogą wyglądać syntetycznie. Zachowaj subtelne różnice odcienia i geometrii wynikające z referencji.

### Włosy i zarost

Zbyt równomierne rozmieszczenie, brak pojedynczych odstających włosów i brak anizotropowego połysku prowadzą do efektu plastikowej bryły.

## Ciało i ruch

Sprawdź:

- sztywną szyję,
- brak oddechu,
- brak drobnego przenoszenia ciężaru,
- gesty rozpoczynające się i kończące idealnie jednocześnie,
- brak ruchu wtórnego włosów i ubrań,
- stałą prędkość ruchu bez przyspieszania i hamowania.

## Okulary

Okulary są silnym elementem identyfikującym twarz. Błędy kilku milimetrów w szerokości, wysokości osadzenia lub pozycji mostka mogą pogarszać podobieństwo. Sprawdź również, czy oprawki nie przecinają brwi, nosa i uszu podczas ekspresji.

## Macierz audytu

Dla każdego problemu zapisuj:

| Pole | Znaczenie |
| --- | --- |
| subsystem | oczy, twarz, mowa, materiały, ciało |
| severity | 1-5 |
| frequency | stały / częsty / sporadyczny |
| camera | close-up / medium / full body |
| reproduction | konkretna poza lub klip |
| suspected_cause | geometria / rig / materiał / timing / eksport |
| fix | proponowana korekta |
| verified | tak / nie |

## Skala istotności

- 1: wykrywalne tylko przy dokładnej inspekcji,
- 2: niewielkie, ale powtarzalne,
- 3: widoczne w normalnym oglądzie,
- 4: silnie obniża wiarygodność postaci,
- 5: natychmiast niszczy iluzję człowieka.

Najpierw naprawiaj problemy 4-5, szczególnie dotyczące oczu, synchronizacji mowy i podobieństwa twarzy.

## Warunki testowe

Audyt wykonuj co najmniej w:

- neutralnym świetle frontalnym,
- świetle bocznym podkreślającym geometrię,
- zbliżeniu twarzy,
- półzbliżeniu podczas mowy,
- pełnej sylwetce w bezczynności i podczas gestu.

## Windows i Linux

Powtarzaj test w docelowym rendererze dla każdej wspieranej platformy. Różnice programu cieniującego lub backendu renderowania należy dokumentować osobno, aby nie pomylić ich z błędami geometrii.

## Kryterium zaliczenia

Awatar przechodzi audyt, gdy nie występują problemy o istotności 4-5, a problemy poziomu 3 są udokumentowane i zaakceptowane jako ograniczenia konkretnego profilu eksportu lub silnika.