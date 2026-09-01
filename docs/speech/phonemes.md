# Fonemy

**Fonem (phoneme)** jest najmniejszą abstrakcyjną jednostką dźwiękową języka, która może rozróżniać znaczenie słów. W animacji awatara fonem nie jest bezpośrednio kształtem ust. Stanowi informację czasową i artykulacyjną, z której wybierany jest odpowiedni wizem (viseme).

Przykładowo fonemy `/p/`, `/b/` i `/m/` różnią się akustycznie, ale wizualnie wymagają podobnego pełnego domknięcia warg, dlatego mogą być mapowane do tej samej klasy wizemu `PP`.

## Fonem a głoska

Fonem opisuje kategorię językową, natomiast rzeczywista realizacja dźwięku w konkretnej wypowiedzi może się zmieniać pod wpływem tempa, akcentu i sąsiednich dźwięków. Dla animacji ważne są więc zarówno symbole fonemów, jak i rzeczywiste czasy ich wystąpienia w wygenerowanym audio.

## Czas trwania fonemu

Nie istnieje jedna poprawna długość fonemu. W szybkiej mowie część segmentów może trwać około 30-60 ms, typowe samogłoski często zajmują około 70-180 ms, a długie lub silnie akcentowane realizacje mogą przekraczać 200 ms.

Zmniejszanie czasu powoduje, że pełna poza wizemu może nie zdążyć się rozwinąć. Wydłużenie pozwala utrzymać cel artykulacyjny dłużej, ale nadmierne wymuszanie pełnej amplitudy może wyglądać teatralnie.

## Wymuszane dopasowanie czasowe

**Wymuszane dopasowanie czasowe (forced alignment)** dopasowuje znany tekst lub sekwencję fonemów do nagrania i wyznacza granice czasowe. Wynik powinien zawierać co najmniej:

- symbol fonemu;
- czas początku;
- czas końca;
- opcjonalną miarę pewności;
- identyfikator pliku audio i jego wersję.

Nie zakładamy, że długość fonemu wynika z liczby liter. Tempo, redukcje i koartykulacja (coarticulation) mogą silnie zmienić realizację.

## Polski profil fonemiczny

Projekt posiada osobny [profil fonemów języka polskiego](polish-phoneme-profile.md). Profil nie zastępuje danych zwracanych przez Piper ani eSpeak NG. Definiuje warstwę normalizującą pomiędzy symbolami narzędzia a klasami artykulacyjnymi używanymi przez Avatar Studio.

## Zasada normalizacji

Nie zapisujemy logiki animacji bezpośrednio pod surowymi symbolami konkretnej wersji narzędzia. Najpierw mapujemy je do kanonicznego symbolu lub klasy fonetycznej Avatar Studio, a dopiero potem do wizemu.

Dzięki temu aktualizacja Piper lub eSpeak NG nie wymaga przebudowy całego facial rigu.

## Artefakt danych

Dane fonemiczne są artefaktem pochodnym i są wersjonowane razem z konkretnym WAV. Zmiana tekstu, modelu głosu, szybkości mowy albo pliku audio unieważnia wcześniejsze czasy fonemów.

Format danych opisuje dokument [Format danych dopasowania czasowego](alignment-format.md).
