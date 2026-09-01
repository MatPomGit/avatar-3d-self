# Web

Wersja webowa jest osobnym profilem środowiska czasu rzeczywistego. Nie jest to strona dokumentacji MkDocs. Demonstrator Web ma być odseparowany od prywatnego obszaru roboczego Avatar Studio i korzystać wyłącznie z jawnie zatwierdzonych artefaktów.

## Format glTF/GLB

glTF jest formatem wymiany zaprojektowanym do efektywnego przenoszenia zasobów 3D. GLB jest jego binarnym wariantem, w którym geometria, dane i często tekstury mogą być umieszczone w jednym pliku.

Dla profilu Web preferujemy GLB, jeśli nie ma technicznego powodu do rozdzielenia zasobów.

## Wiązanie skóry i cele morfowania

Format glTF 2.0 obsługuje wiązanie skóry z kośćmi oraz cele morfowania. Nie oznacza to jednak automatycznie pełnego przeniesienia wszystkich funkcji sceny DCC.

Eksport Web musi jawnie sprawdzić:

- hierarchię kości;
- wagi wpływu;
- wszystkie wymagane cele morfowania;
- nazwy kanałów;
- animacje;
- orientację i jednostki.

## Materiały

Podstawowy model materiałowy glTF jest oparty na modelu metaliczności i chropowatości. To dobrze odpowiada głównemu kontraktowi materiałowemu Avatar Studio, ale zaawansowana skóra, włosy i oczy mogą wymagać rozszerzeń albo implementacji po stronie renderera.

Nie spłaszczamy materiału skóry do prostej tekstury tylko po to, aby plik był zgodny z minimalnym profilem Web. Zamiast tego definiujemy poziom jakości Web i jawnie zapisujemy, które efekty są przybliżone.

## Kompresja

Kompresja może znacznie zmniejszyć rozmiar pobieranego zasobu, ale zwiększa koszt dekodowania i może ograniczać jakość.

Profil Web zapisuje osobno:

- rozmiar niepakowanego modelu;
- rozmiar po kompresji;
- czas pobierania testowego;
- czas dekodowania;
- pamięć po załadowaniu;
- utratę jakości.

Nie oceniamy wydajności Web tylko na podstawie rozmiaru pliku.

## Tekstury

Dla wersji Web szczególnie ważne jest ograniczenie rozdzielczości tekstur i liczby jednocześnie aktywnych map.

LOD0 może zachowywać tekstury wysokiej jakości dla twarzy, ale dalsze poziomy powinny korzystać z niższych rozdzielczości. Strumieniowanie lub progresywne ładowanie jest preferowane, jeżeli demonstrator ma działać przez Internet.

## Animacja mowy

W profilu Web mowa może działać w dwóch trybach:

1. audio i wcześniej obliczone krzywe wizemów;
2. audio oraz dane czasowe fonemów przetwarzane lokalnie do krzywych.

Pierwszy wariant jest prostszy i bardziej deterministyczny dla demonstratora publicznego.

## Prywatność

Demonstrator publiczny nie otrzymuje:

- prywatnego modelu Piper;
- danych treningowych głosu;
- surowych zdjęć referencyjnych;
- prywatnych plików projektu Avatar Studio;
- danych niezatwierdzonych do publikacji.

Może korzystać z wcześniej wygenerowanego audio, jeśli zostało jawnie zatwierdzone jako publiczne.

## Test wydajności

Profil Web testujemy co najmniej na:

- aktualnej przeglądarce Chromium;
- aktualnej przeglądarce Firefox;
- jednym komputerze z wydajnym GPU;
- jednym słabszym urządzeniu;
- połączeniu sieciowym o ograniczonej przepustowości.

Mierzymy czas do pierwszego poprawnie wyświetlonego awatara, czas do pełnej jakości, pamięć, FPS i stabilność animacji.

## Dokumentacja MkDocs

`mkdocs serve` służy wyłącznie do lokalnego podglądu dokumentacji i nie jest demonstratorem Web awatara.

## Kryterium zaliczenia

Profil Web jest zaliczony, jeśli demonstrator ładuje się powtarzalnie, nie ujawnia danych prywatnych, zachowuje najważniejsze cechy podobieństwa oraz stabilnie odtwarza animację twarzy i mowę w zadeklarowanym zakresie sprzętu.