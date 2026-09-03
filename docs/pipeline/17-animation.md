# 17. Animacja

Etap składa klipy w kontrolowany system, zamiast wypalać ruch ciała, oczu i
twarzy w jedną ścieżkę. Kontrakt warstw opisuje [architektura
animacji](../animation/animation-architecture.md), a szczegółowe procedury:
[lokomocja](../animation/locomotion.md), [gesty](../animation/gestures.md),
[spojrzenie](../animation/gaze.md), [mruganie](../animation/blinking.md),
[emocje](../animation/emotions.md), [animacja twarzy](../animation/facial-animation.md)
i [zachowanie w bezczynności](../animation/idle-behaviour.md).

**Input:** zatwierdzony rig/skinning, rest/bind pose, profil eksportu, referencje i
specyfikacja runtime.
**Edytowalny wynik:** klipy źródłowe, warstwy, maski, graf stanów, profil
retargetingu i parametry proceduralne.
**Eksport pochodny:** klipy runtime, skeleton, events/curves i konfiguracja grafu.

## Minimalny zestaw klipów

Utwórz neutralny idle, walk, fast walk, run, start/stop dla obu nóg prowadzących,
turn-in-place L/R, jeden gest rytmiczny i wskazujący oraz testowy klip mowy.
Dla każdego zapisz FPS, długość, loop, kontakty stóp i wariant root motion lub
in-place. Szczegóły podporu, środka ciężkości i diagnostyki slidingu opisuje
[artykuł o lokomocji](../animation/locomotion.md); fazy preparation/stroke/hold/
retraction — [artykuł o gestach](../animation/gestures.md).

## Warstwy, maski i priorytety

Ułóż warstwy: locomotion/base pose → additive idle → upper-body gesture → head
orientation → gaze → blink → facial affect → lip-sync → secondary motion.
Maska `0–1` mówi **gdzie i jak mocno** działa warstwa; priorytet mówi **który
sygnał rozstrzyga konflikt**. Locomotion zachowuje nogi i balans, gest przejmuje
wybrane kości od kręgosłupa do dłoni, gaze steruje oczami z ograniczonym udziałem
głowy, blink ma pierwszeństwo na powiekach, a lip-sync na zwarciach i otwarciu
ust. Emocja nadal steruje brwiami, policzkami i częścią kącików. Reguły regionów
twarzy i clampingu podaje [animacja twarzy](../animation/facial-animation.md).

Maskę buduj od zera, dodając potrzebne kości/kanały; wygasz wpływ na granicy
kręgosłupa zamiast twardego cięcia. Zapisz dla każdej warstwy tryb override lub
additive, referencyjną pozę addytywną, wagę, priorytet i limit. Wyłączaj warstwy
pojedynczo, aby wykryć podwójne sterowanie.

## Przejścia i graf stanów

1. Zbuduj stany idle, start, locomotion, stop i turn oraz warunki prędkości,
   kierunku i nogi podporowej.
2. Synchronizuj przejścia cykli fazą kontaktu. Start/stop kończ pozą zgodną z
   kolejnym stanem; nie maskuj niezgodności długim blendem.
3. Zacznij od blendu `0.15–0.30 s` dla podobnych ruchów i `0.3–0.5 s` dla dużej
   zmiany, po czym oceń ślizganie i bezwładność. Za krótki skacze, za długi daje
   „gumowy” kontakt.
4. Przetestuj przerwanie startu, szybkie odwrócenie kierunku, gest podczas chodu,
   mowę podczas przejścia i powrót do idle.

## Retargeting i root motion

Dopasuj kość root, miednicę, kręgosłup, kończyny i rest pose; różnice proporcji
zapisz w profilu retargetingu. Nie kopiuj translacji dłoni/stóp między różnymi
długościami kości. Po przeniesieniu ponownie sprawdź zakresy stawów, kontakty,
rekwizyty i sylwetkę. Pełną procedurę zawiera [lokomocja](../animation/locomotion.md).

Wybierz jeden kontrakt na klip: root motion przenosi translację/obrót w root,
a in-place pozostawia przemieszczenie logice runtime. Usuń ruch miednicy z root
tylko zgodnie z profilem; runtime nie może jednocześnie zastosować root motion i
prędkości kapsuły. Porównaj przebytą drogę, obrót i pozycję końcową przed/po
eksporcie.

## Gaze i blink

Gaze ma osobny target. Dla małych zmian pracują głównie oczy, dla większych głowa
i tułów; oczy inicjują duży ruch, a głowa dołącza po `70–140 ms`. Nie dodawaj
losowego jitteru. Zakresy fiksacji, sakkad i eyelid follow są w [procedurze
gaze](../animation/gaze.md).

Blink generuj zdarzeniowo, nie periodycznie. Punkt startowy to `12/min`, profil
około `170 ms`, ze zróżnicowanymi odstępami; mowa i zmiana uwagi mogą modulować
częstość. Sprawdź szczelność z każdym kierunkiem spojrzenia zgodnie z [procedurą
mrugania](../animation/blinking.md).

## Test długiego idle

Odtwórz minimum `2 min` bez mowy, następnie `60 s` z gaze targetami i `30 s` z
mową. Idle ma łączyć oddech, postural sway, mikroruchy, zmianę ciężaru, gaze i
blink bez widocznego punktu pętli. Obejrzyj także `4×`: periodyczność i dryf są
wtedy łatwiejsze do wykrycia. Kontrolne zakresy opisuje [idle
behaviour](../animation/idle-behaviour.md). Zaliczenie wymaga nieruchomych stóp,
braku dryfu root, niemechanicznych blinków, celowego gaze, braku kolizji i
poprawnego powrotu każdej warstwy do neutralu.

## Checklisty zamknięcia etapu

### Wejście
- [ ] Rig, skinning, rest/bind pose, skala i profil runtime są zatwierdzone.
- [ ] Referencje i minimalna lista klipów obejmują obie nogi/kierunki.

### Wynik edytowalny
- [ ] Klipy, warstwy, maski, priorytety, przejścia i profil retargetingu są osobne.
- [ ] Parametry gaze/blink/idle oraz znaczniki kontaktu pozostają edytowalne.

### Eksport
- [ ] FPS, loop, events, curves, skeleton i kontrakt root motion są zachowane.
- [ ] Import runtime odtwarza dystans, fazę, nazwy i pozycję końcową.

### Walidacja
- [ ] Wszystkie klipy i przejścia działają osobno, w pętli i w mieszankach.
- [ ] Retargeting, gaze, blink oraz długi idle przeszły w docelowym runtime.

### Błędy blokujące
- [ ] Brak foot slidingu, podwójnego ruchu root, skoków, dryfu i konfliktu masek.
- [ ] Nie ma mechanicznej periodyczności, clippingu ani utraty kontaktu/rekwizytu.

### Definition of Done
- [ ] Minimalny zestaw animacji i graf runtime przechodzą pełną macierz przejść,
      retargeting i długi idle; warstwy można niezależnie edytować, wyciszać i
      eksportować bez błędów blokujących.
