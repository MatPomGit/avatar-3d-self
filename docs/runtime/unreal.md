# Unreal Engine

Unreal Engine jest jednym z docelowych środowisk czasu rzeczywistego Avatar Studio. Profil Unreal nie zmienia wersji wzorcowej postaci. Definiuje sposób importu i odtworzenia jej funkcji w konkretnej wersji silnika.

W raporcie zawsze zapisujemy dokładną wersję Unreal Engine. Nie zakładamy, że ustawienia importu pozostają identyczne między wydaniami.

## Siatka szkieletowa

Siatka szkieletowa (Skeletal Mesh) to deformowalna siatka powiązana ze szkieletem. W Unreal jest podstawową reprezentacją ciała awatara i może zawierać geometrię, wagi wpływu kości, poziomy szczegółowości oraz cele morfowania (morph targets).

Po imporcie weryfikujemy:

- skalę w centymetrach;
- orientację postaci;
- hierarchię kości;
- pozę referencyjną;
- liczbę sekcji materiałowych;
- obecność celów morfowania;
- poziomy szczegółowości.

## Cele morfowania twarzy

Unreal może importować cele morfowania przez potok FBX dla siatek szkieletowych. Nazwy są częścią kontraktu, dlatego nie należy ręcznie zmieniać ich po imporcie.

Dla Avatar Studio wymagamy mapowania 1:1 między nazwą kanału źródłowego a nazwą w silniku, chyba że profil eksportu jawnie definiuje translację.

Testujemy wartości 0, 0,25, 0,5, 0,75 i 1 po stronie logicznej Avatar Studio. Jeżeli interfejs silnika używa innej reprezentacji liczbowej, adapter wykonuje konwersję.

## Materiały skóry

Materiał skóry musi odtwarzać:

- barwę bazową;
- chropowatość;
- mapy normalnych;
- rozpraszanie podpowierzchniowe;
- mikrodetal;
- dynamiczne zmarszczki, jeżeli są aktywne w danym profilu.

Nie kopiujemy wartości parametrów ślepo między Blenderem i Unreal. Dwa programy mogą używać innego modelu cieniowania lub skali parametru artystycznego.

## Oczy

Oko jest testowane jako oddzielny układ optyczny. Weryfikujemy:

- wypukłą rogówkę;
- refleks z rogówki;
- tęczówkę z głębią;
- źrenicę;
- menisk łzowy;
- kontakt z powiekami.

Jeżeli koszt pełnego załamania światła jest zbyt duży, profil Unreal może stosować kontrolowane przybliżenie, ale musi zostać ono opisane w raporcie.

## Włosy

Profil może używać systemu włosów albo płaszczyzn z teksturą włosów. Dobór zależy od docelowego sprzętu i poziomu szczegółowości.

Weryfikujemy osobno:

- gęstość;
- cienie;
- ruch wtórny;
- kolizje;
- zmianę LOD;
- koszt GPU.

## Animacja

Klip akceptacyjny obejmuje:

- pozycję neutralną;
- chód;
- ruchy rąk;
- pełny zakres palców;
- ruch oczu;
- mruganie;
- ekspresje;
- mowę.

## Windows

1. Utwórz czysty projekt walidacyjny dla przypiętej wersji Unreal Engine.
2. Zaimportuj artefakt pochodny z włączonym importem celów morfowania.
3. Zweryfikuj skalę, szkielet i pozę referencyjną.
4. Odtwórz materiały skóry, oczu, włosów, ubrań i okularów.
5. Uruchom klipy akceptacyjne.
6. Wykonaj pomiar CPU, GPU i pamięci.
7. Zapisz raport importu.

## Linux

1. Użyj tej samej wersji projektu i tego samego artefaktu wejściowego.
2. Zweryfikuj różnice backendu renderera i sterownika.
3. Porównaj siatkę, cele morfowania i materiały z profilem Windows.
4. Sprawdź obsługę włosów i przezroczystości.
5. Uruchom identyczne klipy akceptacyjne.
6. Zapisz osobny raport wydajności.

## MetaHuman

Nie traktujemy zgodności z MetaHuman jako cechy automatycznej. Jeżeli projekt będzie mapowany do standardu MetaHuman, powstanie osobna decyzja architektoniczna opisująca wymagania szkieletu, twarzy, nazw kanałów i ograniczenia przenoszenia danych.

## Kryterium zaliczenia

Profil Unreal jest zatwierdzony, jeśli import zachowuje podobieństwo, pełną podstawową mimikę, mowę, poprawną deformację ciała oraz osiąga budżet wydajności na zadeklarowanym sprzęcie.