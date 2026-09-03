# Lokomocja

Lokomocja (locomotion) jest bazową warstwą ruchu całego ciała. Musi zachować
kontakt z podłożem, wiarygodne przenoszenie ciężaru i możliwość przenoszenia
animacji między szkieletami (animation retargeting), a jednocześnie pozostawać
niezależna od warstw twarzy, spojrzenia i mowy. Widz wybaczy drobną różnicę w
ułożeniu palców, ale natychmiast zauważy stopę sunącą po ziemi. Dlatego pracę nad
lokomocją zaczynamy od podporu i ciężaru ciała, a dopiero później dopracowujemy
ozdobne ruchy tułowia i kończyn.

## Wymagania wstępne i dane wejściowe

Przygotuj zatwierdzoną geometrię, szkielet (skeleton) z hierarchią i osiami kości,
układ sterowania postacią (rig), wiązanie skóry z kośćmi (skinning), rzeczywistą
skalę sceny, specyfikację środowiska wykonawczego (runtime) oraz referencję chodu.
Minimalny zestaw docelowy obejmuje animację bezczynności
(idle animation), chód, szybki chód, bieg, obrót w miejscu, start, stop i
podstawowe przejścia.

Przed animowaniem sprawdź materiały tak, jak sprawdza się narzędzia przed pracą.
Jeśli skala, długość nóg albo osie kości są błędne, nawet starannie wykonany chód
będzie wymagał ciągłych poprawek. Referencję oglądaj zarówno w normalnym tempie,
aby ocenić charakter ruchu, jak i klatka po klatce, aby zobaczyć podpory.

## Procedura przygotowania

1. **Ustal pozę spoczynkową.** Poza spoczynkowa (rest pose) ma być zgodna ze
   sceną źródłową, bez niezamierzonych translacji i skal kości. Zapisz osobno pozę
   wiązania (bind pose), jeśli format ją rozróżnia. Sprawdź osie lokalne, hierarchię,
   kość korzenia, długości kończyn i symetrię nazw; nie poprawiaj szkieletu dopiero
   w klipie animacji. Poza spoczynkowa jest miarką, według której system porównuje
   oba szkielety; krzywa miarka daje krzywy wynik w każdym klipie.
2. **Wybierz sposób przemieszczenia.** Ruch korzenia (root motion) zapisuje
   translację i obrót postaci w animacji; wybierz go dla precyzyjnie reżyserowanych
   startów, zatrzymań i obrotów. Animacja w miejscu (in-place animation) pozostawia
   root w miejscu, a prędkość nadaje runtime; wybierz ją dla sterowania gracza.
   W pierwszym wariancie animacja „ciągnie” postać przez świat, w drugim postać
   idzie jak na bieżni, a przesuwa ją logika gry. Nie mieszaj obu sposobów w jednym
   zestawie bez jawnej konwersji i testu, bo postać może przesunąć się podwójnie.
3. **Utwórz cykl chodu.** Zbuduj kolejne kontakty, obniżenia, mijania i uniesienia
   dla lewej i prawej nogi. Pierwsza oraz ostatnia klatka muszą tworzyć ciągłą
   pętlę; nie duplikuj ich przy odtwarzaniu. Dopasuj rotację miednicy, przeciwfazę
   ramion i ruch wtórny bez naruszania czytelności podporu.
4. **Oznacz kontakty.** Dodaj znaczniki kontaktu pięty, pełnego podparcia i wybicia
   palców dla obu stóp. W czasie podporu zablokuj pozycję stopy względem podłoża;
   pozycję rozwiązuj z biodra i kolana, a nie przesuwaniem stopy. Traktuj stopę
   podporową jak pinezkę przypinającą postać do podłoża: reszta ciała porusza się
   wokół niej aż do wybicia palców.
5. **Skoryguj środek ciężkości.** Środek ciężkości (center of gravity) powinien
   przechodzić nad aktywną podporą. Kontroluj wysokość i przesunięcie boczne
   miednicy; zbyt małe przeniesienie wygląda nieważko, a zbyt duże kołysze postać.
   Jeśli nie masz pewności, zatrzymaj klip w połowie podporu i sprawdź, czy postać
   mogłaby utrzymać tę pozę bez przewrócenia się.
6. **Przygotuj start, stop i obrót.** Dla obu nóg prowadzących utwórz start ze
   spoczynku, zatrzymanie i obrót w miejscu. Oznacz fazy podporu, wyhamowanie oraz
   docelowy kąt. Każdy klip zakończ pozą zgodną z wejściem następnego stanu.
7. **Wykonaj retargeting.** Zmapuj kość korzenia, miednicę, kręgosłup i kończyny,
   używając zgodnych póz spoczynkowych. Skoryguj różnice proporcji w profilu
   retargetingu, po czym ponownie sprawdź kontakty; nie kopiuj bezpośrednio
   translacji kończyn między szkieletami o innych długościach.
8. **Skonfiguruj runtime.** Dodaj stany idle, start, locomotion, stop i turn.
   Przejście między animacjami (animation blend) uzależnij od prędkości, kierunku,
   nogi podporowej i żądania obrotu. Użyj synchronizacji fazy chodu, łagodnych
   krzywych przejść i masek dla gestów górnej części ciała. Potwierdź, że runtime
   nie stosuje prędkości kapsuły jednocześnie z root motion.

## Oczekiwany wynik i walidacja

Wynikiem jest edytowalny zestaw klipów, profil retargetingu, znaczniki kontaktów
i konfiguracja runtime. Odtwórz każdy klip osobno, w pętli i we wszystkich
przejściach; testuj oba kierunki, różne prędkości, pochyłość docelowego podłoża i
docelową liczbę klatek na sekundę. Porównaj przebytą odległość z długością kroku,
wykres wysokości kości korzenia (root bone) z miednicą oraz wynik przed i po
retargetingu.

## Diagnostyka

Nie poprawiaj od razu pierwszej krzywej, która wygląda podejrzanie. Najpierw
ustal, **kiedy** pojawia się błąd: w surowym klipie, po retargetingu czy dopiero
w runtime. Ten sam efekt wizualny może mieć różne przyczyny — ślizganie stopy
może wynikać zarówno ze złej pozycji stopy, jak i z niedopasowanej prędkości.

| Objaw | Jak potwierdzić przyczynę | Naprawa |
| --- | --- | --- |
| Ślizganie stóp (foot sliding) | Wyświetl tor kontaktowej stopy i porównaj prędkość klipu z prędkością postaci. Ruch toru oznacza błędny kontakt; różne prędkości oznaczają niedopasowanie napędu. | Zablokuj stopę w fazie podporu, popraw znaczniki i IK; dopasuj prędkość runtime do root motion albo przeskaluj czas/długość kroku dla in-place. |
| Zła długość kroku (incorrect stride length) | Zmierz odległość kolejnych kontaktów i porównaj ją z proporcjami nóg oraz prędkością. | Skoryguj pozycje kontaktów z biodra, czas cyklu lub prędkość; po retargetingu użyj profilu proporcji zamiast skalować samą stopę. |
| Podskakiwanie kości korzenia (root bone bouncing) | Porównaj wykres pionowy root bone i miednicy; identyczne oscylacje wskazują, że ruch miednicy zdublowano w root. | Pozostaw lokomocyjną translację na root, a pionową pracę chodu na miednicy; wygładź krzywą bez spłaszczania naturalnego środka ciężkości. |
| Penetracja podłoża (ground penetration) | Sprawdź wysokość pięty i palców w kontaktach, osie, skalę oraz dopasowanie stopy przez kinematykę odwrotną (Inverse Kinematics, IK) na pochyłości. | Popraw wysokość kontaktu i orientację stopy, ujednolić jednostki, ustaw przesunięcie podeszwy i ograniczenia IK dla docelowego podłoża. |

Jeśli błąd pojawia się dopiero w runtime, najpierw odtwórz surowy klip bez
przejść, IK i skalowania prędkości. Następnie włączaj kolejno retargeting,
przejście, dopasowanie stóp i sterowanie kapsułą. Pozwala to znaleźć etap, który
wprowadza błąd, bez destrukcyjnej korekty klipu źródłowego.

## Kryteria ukończenia

- Poza spoczynkowa, szkielet, skala i wybrany sposób przemieszczenia są zapisane.
- Cykle są ciągłe, a obie stopy pozostają nieruchome podczas oznaczonego podporu.
- Start, stop i obrót działają dla obu nóg prowadzących oraz łączą się bez skoku.
- Retargeting zachowuje kontakty, środek ciężkości i zakresy stawów.
- Wszystkie przejścia runtime działają przy docelowych prędkościach bez slidingu,
  podskakiwania root bone ani penetracji podłoża.
- Warstwy gestów, spojrzenia i twarzy nie wyłączają równowagi ani lokomocji.
