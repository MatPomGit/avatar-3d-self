# Środowisko czasu rzeczywistego

Środowisko czasu rzeczywistego (runtime environment) jest miejscem, w którym gotowy awatar jest faktycznie wyświetlany, animowany i sterowany. To na tym etapie weryfikujemy, czy postać zachowała wygląd, proporcje, materiały, układ sterowania postacią (rig), kształty deformacyjne (blend shapes), animację mowy i zakładany poziom wydajności po opuszczeniu programu DCC.

Sukces eksportu pliku nie oznacza jeszcze sukcesu wdrożenia. Ten sam model może wyglądać poprawnie w Blenderze, a po imporcie do silnika mieć inną skalę, źle zinterpretowane mapy normalnych, odwróconą oś kości, zmienione materiały albo brak części kształtów deformacyjnych.

## Wersja wzorcowa i artefakty pochodne

Wersja wzorcowa (master asset) pozostaje edytowalnym źródłem prawdy. Pliki FBX, GLB, glTF lub inne formaty pośrednie są artefaktami pochodnymi (derived artifacts). Nie wolno poprawiać błędu wyłącznie w wyeksportowanym pliku, jeżeli ta sama poprawka powinna istnieć w wersji wzorcowej.

W praktyce oznacza to:

- błąd geometrii poprawiamy w źródle;
- błąd mapowania materiału poprawiamy w profilu eksportu lub materiale źródłowym;
- błąd specyficzny wyłącznie dla silnika może być naprawiony po stronie adaptera silnika;
- każda ręczna poprawka w środowisku docelowym musi być możliwa do odtworzenia.

## Pakiet importowy

Pakiet importowy powinien zawierać co najmniej:

1. siatkę lub zestaw siatek;
2. szkielet i wagi wpływu kości;
3. kształty deformacyjne twarzy;
4. animacje testowe;
5. tekstury i opis przestrzeni barw;
6. materiały lub dane pozwalające je odtworzyć;
7. konfigurację wizemów;
8. informacje o skali, osiach i jednostkach;
9. profil eksportu;
10. raport konwersji z sumami kontrolnymi plików.

## Profil eksportu

Profil eksportu (export profile) to jawny zestaw reguł przekształcających wersję wzorcową do konkretnego środowiska docelowego. Powinien określać między innymi jednostki, orientację osi, format map normalnych, nazwy materiałów, sposób pakowania tekstur, obsługę kształtów deformacyjnych oraz poziomy szczegółowości.

Zmiana profilu eksportu może zmienić wygląd awatara nawet bez zmiany samego modelu. Dlatego profil należy wersjonować tak samo jak inne elementy produkcyjne.

## Kolejność walidacji

Po eksporcie wykonujemy walidację w tej kolejności:

1. skala i orientacja;
2. hierarchia szkieletu;
3. deformacja ciała;
4. kształty deformacyjne twarzy;
5. materiały i tekstury;
6. włosy i zarost;
7. animacja mowy;
8. poziomy szczegółowości;
9. wydajność;
10. stabilność długiego działania.

Dzięki temu błąd materiału nie maskuje błędu geometrii, a problem wydajności nie jest analizowany zanim postać zostanie poprawnie zaimportowana.

Zobacz kolejno: [budżet wydajności](performance-budget.md), [poziomy szczegółowości](lod.md), [walidację importu](import-validation.md), [Unreal Engine](unreal.md), [Unity](unity.md) i [Web](web.md).