# Okulary

Okulary są osobnym obiektem 3D i ważnym elementem podobieństwa twarzy. Błąd szerokości oprawki o kilka milimetrów, niewłaściwy mostek albo niepoprawne położenie soczewek może zmienić odbiór proporcji oczu i nosa bardziej niż drobny błąd tekstury skóry.

## Geometria oprawek

Model powinien być oparty na pomiarach rzeczywistych okularów. Minimum pomiarowe:

- szerokość całego frontu;
- szerokość pojedynczej soczewki;
- wysokość soczewki;
- szerokość mostka;
- długość zauszników;
- grubość oprawki w kilku charakterystycznych miejscach;
- odległość soczewki od rogówki w pozycji neutralnej.

Dla wymiarów liniowych przyjmujemy cel błędu poniżej 1 mm, a dla bardzo małych detali poniżej 0,5 mm, jeśli pomiar jest wiarygodny.

## Współczynnik załamania światła

**Współczynnik załamania światła (Index of Refraction, IOR)** opisuje zmianę kierunku światła przy przejściu między ośrodkami. Wartość około 1,0 oznacza prawie brak załamania względem powietrza, około 1,33 odpowiada wodzie, około 1,50 jest typowa dla wielu szkieł i tworzyw optycznych, a soczewki o podwyższonym współczynniku mogą przekraczać 1,60.

Dla neutralnej soczewki demonstracyjnej Avatar Studio przyjmujemy `IOR = 1,50` jako wartość startową. Jeżeli znany jest rzeczywisty materiał soczewek, profil powinien użyć wartości zmierzonej lub podanej przez producenta.

Zbyt niski IOR daje zbyt słabe załamanie i „płaską” soczewkę. Zbyt wysoki powoduje nadmierne przesunięcie obrazu oka i nienaturalne refleksy na krawędziach.

## Chropowatość soczewki

Czysta soczewka ma bardzo niską chropowatość (roughness). Typowy punkt startowy to `0,01-0,04` w modelu GGX. Wartości około `0,08-0,15` mogą symulować zabrudzenie albo zmatowienie, ale nie powinny być używane jako domyślny materiał okularów.

## Powłoka antyrefleksyjna

Powłoki antyrefleksyjne zmniejszają widoczność części odbić i często wprowadzają słabe zależne od kąta zabarwienie. W środowisku czasu rzeczywistego nie należy symulować ich przez stałe niebieskie zabarwienie całej soczewki. Efekt powinien być subtelny i zależny od kąta obserwacji.

## Grubość soczewki

Soczewka nie może być pojedynczą powierzchnią bez grubości, jeśli środowisko docelowe używa refrakcji. Dla zwykłych okularów korekcyjnych grubość może wynosić od około 1 mm w cienkich obszarach do kilku milimetrów przy krawędziach, zależnie od korekcji i materiału.

Jeżeli nie znamy mocy optycznej prawdziwej soczewki, nie próbujemy jej odtwarzać na podstawie wyglądu. Priorytetem jest geometria oprawki i wizualnie wiarygodna soczewka o neutralnej mocy.

## Położenie względem twarzy

Okulary powinny być związane z kością głowy, ale ich położenie jest kalibrowane względem nosa, uszu i oczu. Należy sprawdzić:

- kontakt nosków z nosem;
- położenie zauszników przy uszach;
- brak kolizji z brwiami podczas ekspresji;
- brak penetracji rzęs przez soczewkę;
- stabilność przy ruchach głowy.

## Poziomy szczegółowości

Dla poziomu szczegółowości LOD0 zachowujemy pełną geometrię soczewek, zawiasów i głównych detali. Dalsze poziomy mogą upraszczać zawiasy i drobne elementy, ale nie mogą zmieniać charakterystycznego konturu oprawki.

## Definition of Done

Okulary zaliczają etap, jeśli:

- podstawowe wymiary odpowiadają referencji;
- soczewki i oprawki są osobną geometrią;
- materiał soczewki ma fizycznie wiarygodny IOR i chropowatość;
- brak nierealistycznego stałego zabarwienia refleksów;
- nie występują kolizje z twarzą, brwiami i rzęsami;
- kontur oprawek jest stabilny między poziomami szczegółowości.
