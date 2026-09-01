# Fotogrametria: przygotowanie i opis zdjęć

> Cel: zebrać spójny zestaw ostrych zdjęć, z których program rozpozna wspólne punkty na twarzy i sylwetce. Nie zmieniaj jednocześnie oświetlenia, pozy, ogniskowej ani odległości od fotografowanej osoby.

## 1. Przygotuj stanowisko

1. Wybierz jasne, równomierne światło rozproszone. Stań przy dużym oknie w pochmurny dzień albo użyj dwóch miękkich źródeł światła z lewej i prawej strony.
2. Wyłącz automatyczny flash. Nie używaj światła punktowego, kolorowego ani migającego.
3. Ustaw jednolite, matowe tło oddalone co najmniej 1 m od osoby. Tło nie może być błyszczące ani mieć powtarzalnego wzoru.
4. Poproś osobę o nieruchome stanie, neutralny wyraz twarzy i zamknięte usta. Włosy, broda i okulary pozostają w docelowym wyglądzie.
5. Usuń ruchome dodatki. Nie zmieniaj ubrania, fryzury ani położenia okularów w trakcie jednej serii.

**Zatrzymaj się:** jeżeli na twarzy są ostre cienie, odbicia w soczewkach albo ruch, popraw stanowisko przed wykonaniem zdjęć.

## 2. Ustaw aparat

1. Użyj jednego aparatu lub jednego telefonu dla całej serii.
2. Wybierz obiektyw standardowy, nie ultraszerokokątny. W telefonie wybierz główną kamerę 1x.
3. Wyłącz filtr upiększający, tryb portretowy, HDR zmieniający klatki oraz zoom cyfrowy.
4. Ustaw najwyższą dostępną jakość JPEG albo RAW. Zachowaj oryginalne pliki.
5. Zablokuj ekspozycję, balans bieli i ostrość na twarzy, jeżeli aparat to umożliwia.
6. Nie zmieniaj ogniskowej, rozdzielczości ani proporcji obrazu podczas serii.

## 3. Wykonaj serię twarzy

### Wybierz sposób zmiany widoku

Możesz obejść osobę z kamerą albo zostawić kamerę nieruchomo i obracać osobę. Nie łącz tych metod w jednej serii.

**Wariant A: operator obchodzi osobę.** Osoba stoi nieruchomo. Operator porusza się po łuku o stałym promieniu i wykonuje zdjęcie co 10-15 stopni. To wariant preferowany, gdy dostępna jest druga osoba.

**Wariant B: zdjęcia wykonywane samodzielnie.** Umieść telefon lub aparat na stabilnym statywie. Ustaw znacznik na podłodze pod stopami. Po każdym zdjęciu obróć całe ciało o około 10-15 stopni wokół własnej osi, bez przesuwania stóp poza znacznik i bez pochylania głowy. Do kontroli kąta użyj naklejonych na podłodze znaczników albo powtarzalnej liczby małych kroków. Uruchom samowyzwalacz 3-10 s lub zdalny spust.

W wariancie B aparat pozostaje na tej samej wysokości i w tej samej odległości. Aby wykonać drugi i trzeci pierścień, po ukończeniu pełnego obrotu zmień wyłącznie wysokość statywu, a następnie powtórz pełny obrót osoby.


1. Ustaw obiektyw 0,8-1,2 m od twarzy i na wysokości oczu.
2. Zrób pierwszy pierścień. W wariancie A obejdź osobę po łuku; w wariancie B osoba obraca się na znaczniku. Wykonuj zdjęcie co 10-15 stopni. Każde kolejne zdjęcie ma pokazywać co najmniej 70% poprzedniego kadru.
3. Zrób drugi pierścień z aparatem około 20 cm wyżej, skierowanym lekko w dół.
4. Zrób trzeci pierścień z aparatem około 20 cm niżej, skierowanym lekko w górę.
5. Wykonaj zdjęcia kontrolne czoła, uszu, nosa, brody, linii włosów i szyi. Każdy detal ma być widoczny na kilku zdjęciach z różnych kierunków.
6. Nie fotografuj tylko przodu twarzy. Program nie odtworzy poprawnie boków, uszu i żuchwy bez pokrycia wielowidokowego.

## 4. Wykonaj serię sylwetki

1. Umieść osobę 1-2 m od tła. Zostaw margines nad głową i pod stopami.
2. Ustaw pozę A-pose: ręce odsunięte od tułowia o około 30-45 stopni, palce rozstawione, stopy równolegle na szerokość bioder.
3. Wykonaj pełny okrąg: operator obchodzi osobę albo osoba obraca się na znaczniku. Wykonuj zdjęcie co 10-15 stopni na wysokości klatki piersiowej.
4. Powtórz pełny okrąg z aparatem wyżej i niżej. Nie skracaj serii dla rąk, pach, szyi, bioder i stóp.
5. Zrób dodatkowe zbliżenia dłoni: grzbiet, wnętrze, oba boki i każdy palec. Palce nie mogą zasłaniać się wzajemnie.
6. Zrób osobne zbliżenia butów, uszu, okularów i ubrań, jeżeli mają być modelowane.

## 5. Kontroluj jakość przed zakończeniem

Dla każdego zdjęcia sprawdź: ostrość na osobie, brak poruszenia, stałą ekspozycję, brak obciętych części ciała i wystarczające pokrycie z sąsiednimi kadrami.

Odrzuć zdjęcie, gdy: twarz jest nieostra, osoba mrugnęła, zmieniła pozę, obiekt został zasłonięty, wystąpił silny odblask albo zdjęcie ma inną ogniskową.

## 6. Nazwij i opisz pliki

1. Skopiuj oryginały do prywatnego katalogu bez automatycznej optymalizacji.
2. Utwórz katalogi `face/`, `body/`, `hands/`, `details/` i `rejected/`.
3. Nazwij pliki małymi literami, na przykład `face_ring_01.jpg`, `body_high_12.jpg`, `hands_left_palm_03.jpg`. Zachowaj kolejność obrotu.
4. Utwórz plik `capture_manifest.json`. Zapisz datę, użyte urządzenie, ogniskową lub kamerę, rozdzielczość, typ oświetlenia, odległość od osoby, liczbę zdjęć i uwagi o okularach, włosach oraz ubraniu.
5. Nie publikuj zdjęć, metadanych lokalizacyjnych ani manifestu zawierającego dane osobowe w publicznym repozytorium.

## 7. Wykonaj próbę rekonstrukcji

1. Uruchom rekonstrukcję na kopii zestawu zdjęć.
2. Obejrzyj chmurę punktów i mesh.
3. Zaznacz brakujące fragmenty, na przykład ucho, spód brody, dłonie albo bok okularów.
4. Dograj tylko brakujące widoki w identycznym świetle i z tą samą konfiguracją aparatu.
5. Powtórz rekonstrukcję. Nie maskuj braków przypadkowymi zdjęciami z innego dnia.

## Lista końcowa

- co najmniej trzy pierścienie zdjęć twarzy;
- pełne pokrycie sylwetki na trzech wysokościach;
- dodatkowe zbliżenia dłoni, uszu, okularów i detali;
- stałe światło, ogniskowa i poza;
- ostre zdjęcia z dużym pokryciem;
- prywatnie przechowywane oryginały i opis zestawu.
