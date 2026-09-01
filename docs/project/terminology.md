# Słownik terminologiczny

Ten dokument jest kanonicznym słownikiem terminów używanych w dokumentacji Avatar Studio. Jego celem jest zachowanie poprawnej polszczyzny technicznej bez utraty zgodności z anglojęzycznymi narzędziami, publikacjami i interfejsami API.

## Zasada redakcyjna

W tekście objaśniającym najpierw podajemy poprawny polski termin, a następnie angielski odpowiednik w nawiasie, na przykład **przestrzeń barw (color space)**. Nie tworzymy sztucznych kalek językowych, jeśli istnieje utrwalony polski odpowiednik.

Wyjątkiem są identyfikatory będące częścią kontraktu technicznego, na przykład `roughness`, `jawOpen`, `BaseColor`, nazwy współczynników ARKit, nazwy pól JSON, nazwy parametrów programu lub ścieżki plików. W takich przypadkach identyfikator pozostaje bez zmian, a jego znaczenie wyjaśnia tekst otaczający.

Jeżeli termin nie ma dobrze utrwalonego polskiego odpowiednika, stosujemy opisową polską nazwę i zachowujemy termin angielski w nawiasie. Nie spolszczamy nazw standardów, formatów i produktów.

## Zasada pierwszego użycia pojęcia

Nowe pojęcie nie może pojawić się po raz pierwszy wyłącznie jako nazwa parametru, skrót albo wartość w tabeli. Przy pierwszym użyciu w danym rozdziale należy krótko wyjaśnić:

1. **czym jest pojęcie**, najlepiej jednym lub dwoma zdaniami wprowadzającymi;
2. **co zmienia w praktyce**, czyli jaki efekt wizualny, geometryczny, fizyczny lub wydajnościowy powoduje zwiększenie albo zmniejszenie wartości;
3. **jakie wartości może przyjmować**, z co najmniej jednym przykładem wartości niskiej, typowej i wysokiej, jeśli parametr jest liczbowy;
4. **kiedy stosuje się poszczególne wartości**, np. dla skóry, szkła, włosów, zbliżenia twarzy, dalszego poziomu szczegółowości albo innego środowiska docelowego;
5. **jak rozpoznać wartość błędną**, jeśli zbyt mała lub zbyt duża wartość prowadzi do charakterystycznego artefaktu.

Przykład: zamiast pisać tylko „IOR rogówki = 1,376”, należy najpierw wyjaśnić, że **współczynnik załamania światła (Index of Refraction, IOR)** opisuje zmianę kierunku światła przy przejściu między ośrodkami. Wartość około 1,0 oznacza praktycznie brak załamania względem próżni lub powietrza, około 1,33 jest typowa dla wody, około 1,38 dla rogówki, a około 1,5 dla wielu rodzajów szkła. Zwiększenie IOR wzmacnia załamanie i zmienia zachowanie odbić Fresnela.

## Renderowanie i materiały

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| renderowanie oparte na fizyce | Physically Based Rendering, PBR | Kanoniczne rozwinięcie PBR. |
| model metaliczności i chropowatości | metallic-roughness workflow | Dotyczy modelu materiałowego PBR. |
| barwa bazowa | Base Color | Dla tekstury wejściowej można także używać terminu albedo, jeśli dane rzeczywiście reprezentują albedo. |
| albedo | albedo | Termin naukowy używany również po polsku. |
| chropowatość | roughness | Parametr mikrogeometrycznego rozpraszania odbicia. |
| metaliczność | metallic | Parametr rozróżniający zachowanie metalu i dielektryka w modelu PBR. |
| mapa normalnych | normal map | Nie używać „normal mapa”. |
| mapa wysokości | height map | Dane wysokości powierzchni. |
| mapa przemieszczeń | displacement map | Steruje rzeczywistym lub pozornym przemieszczeniem powierzchni. |
| mapa okluzji otoczenia | Ambient Occlusion map, AO | Skrót AO może pozostać po pełnym rozwinięciu. |
| mapa przezroczystości | opacity map | Dla kanału alfa używać osobno „kanał alfa (alpha channel)”. |
| mapa emisji | emissive map | Dla powierzchni emitujących światło. |
| rozpraszanie podpowierzchniowe | Subsurface Scattering, SSS | Dla skóry, wosku i innych materiałów półprzezroczystych. |
| współczynnik załamania światła | Index of Refraction, IOR | Wielkość bezwymiarowa. |
| współczynnik odbicia Fresnela dla padania prostopadłego | normal-incidence Fresnel reflectance, F0 | Stosować symbol F0. |
| dwukierunkowa funkcja rozkładu odbicia | Bidirectional Reflectance Distribution Function, BRDF | Termin optyczny. |
| powłoka antyrefleksyjna | anti-reflective coating | Powłoka ograniczająca część odbić na granicy ośrodków optycznych. |
| program cieniujący | shader | W kontekście konkretnego silnika można mówić o module lub programie cieniującym. |
| model cieniowania | shading model | Nie utożsamiać z programem cieniującym. |
| przestrzeń barw | color space | Termin stosowany w grafice komputerowej i poligrafii. |
| zarządzanie barwą | color management | Dotyczy profili, transformacji i zgodności barw. |
| profil barwny | color profile | Dla ICC: profil ICC. |
| funkcja przenoszenia | transfer function | Np. sRGB. |
| dane liniowe | linear data | Dane bez nieliniowej funkcji kodującej barwę. |
| głębia bitowa | bit depth | Liczba bitów przeznaczona na zapis próbki lub kanału. |
| liczba zmiennoprzecinkowa | floating-point value | W teksturach np. 16-bit float lub 32-bit float. |
| kompresja stratna | lossy compression | |
| kompresja bezstratna | lossless compression | |
| łańcuch mipmap | mipmap chain | Zestaw kolejnych poziomów rozdzielczości tekstury. |
| filtrowanie anizotropowe | anisotropic filtering | |

## UV i tekstury

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| współrzędne UV | UV coordinates | |
| rozwinięcie UV | UV unwrapping | Proces tworzenia odwzorowania powierzchni 3D na płaszczyznę. |
| wyspa UV | UV island | Spójny fragment rozwinięcia UV. |
| szew UV | UV seam | Krawędź rozcięcia rozwinięcia. |
| system kafli tekstur UDIM | UDIM texture tiling | UDIM pozostaje nazwą standardu numeracji kafli. |
| kafel UDIM | UDIM tile | Np. 1001. |
| gęstość tekseli | texel density | Liczba tekseli przypadająca na jednostkę długości powierzchni modelu. |
| teksel | texel | Element tekstury, analogiczny do piksela obrazu. |
| margines między wyspami UV | UV padding | W kontekście wypalania można także używać „margines wypalania (bake padding)”. |
| margines wypalania | bake padding | Rozszerzenie danych poza granice wyspy UV. |
| wypalanie tekstur | texture baking | Przenoszenie informacji między reprezentacjami powierzchni. |
| rozdzielczość tekstury | texture resolution | |
| próbkowanie tekstury | texture sampling | |

## Geometria i modelowanie

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| siatka wielokątów | polygon mesh | W skrócie: siatka. |
| siatka wysokiej rozdzielczości | high-poly mesh | |
| siatka niskiej rozdzielczości | low-poly mesh | |
| retopologia | retopology | Termin utrwalony w grafice 3D. |
| przepływ krawędzi | edge flow | Opis topologii krawędzi wokół deformowanych obszarów. |
| czworokąt | quad | |
| trójkąt | triangle | |
| wierzchołek | vertex | |
| krawędź | edge | |
| ściana | face | |
| geometria niebędąca rozmaitością | non-manifold geometry | Można skrócić do „geometria non-manifold” tylko w kodzie lub nazwie narzędzia. |
| obwiednia | bounding box | Dla osiowej: osiowo wyrównana obwiednia prostopadłościenna (axis-aligned bounding box, AABB). |
| poziom szczegółowości | Level of Detail, LOD | Skrót LOD jest dopuszczalny po rozwinięciu. |

## Włosy i zarost

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| system włosów | groom | Obejmuje dane opisujące włosy, prowadnice i parametry generowania. |
| prowadnica włosów | guide strand | |
| włos renderowany | render strand | |
| płaszczyzna z teksturą włosów | hair card | Unikamy samej kalki „karta włosów” w tekście dydaktycznym. |
| grupowanie pasm | clumping | |
| pojedyncze odstające włosy | flyaway hairs | |
| linia włosów | hairline | |
| skóra głowy | scalp | |
| model anizotropowego odbicia włosa | anisotropic hair shading model | |
| chropowatość wzdłużna | longitudinal roughness | |
| chropowatość azymutalna | azimuthal roughness | |

## Rigowanie i deformacja

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| szkielet | skeleton | |
| rig | rig | Termin branżowy pozostaje dopuszczalny; w tekście dydaktycznym: „układ sterowania postacią (rig)”. |
| układ sterowania | control rig | |
| kość deformująca | deformation bone | |
| kość skrętna | twist bone | |
| kinematyka prosta | Forward Kinematics, FK | |
| kinematyka odwrotna | Inverse Kinematics, IK | |
| wiązanie skóry z kośćmi | skinning | Przy kolejnych użyciach dopuszczalne „skinning” tylko w nazwach narzędzi i plików. |
| waga wpływu kości | skin weight | |
| klucz kształtu | shape key | Nazwa używana przez Blender. |
| kształt deformacyjny | blend shape | Ogólny termin interoperacyjny. |
| cel morfowania | morph target | Termin używany m.in. przez silniki czasu rzeczywistego. |
| kształt korekcyjny | corrective shape | |
| poza spoczynkowa | rest pose | |
| poza wiązania | bind pose | |
| przenoszenie animacji między szkieletami | animation retargeting | |

## Animacja i zachowanie

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| animacja bezczynności | idle animation | |
| ruch wtórny | secondary motion | |
| ruch główny | primary motion | |
| ruch korzenia | root motion | |
| przejście między animacjami | animation blend | |
| warstwa addytywna | additive layer | |
| maska animacji | animation mask | |
| sakkada | saccade | Termin fizjologiczny. |
| mikrosakkada | microsaccade | |
| fiksacja wzroku | gaze fixation | |
| śledzenie powiek za ruchem oka | eyelid follow | |
| mrugnięcie | blink | |
| czas narastania | onset time | Dla ekspresji i sygnałów. |
| faza maksymalnego nasilenia | apex | |
| czas wygaszania | offset time | |

## Twarz i mowa

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| jednostka działania mięśniowego | Action Unit, AU | W systemie FACS. |
| fonem | phoneme | |
| wizem | viseme | Utrwalony termin dla wizualnego odpowiednika fonemu. |
| koartykulacja | coarticulation | Forma preferowana w dokumentacji projektu. |
| wymuszane dopasowanie czasowe | forced alignment | Dopasowanie transkrypcji/fonemów do sygnału mowy. |
| miara pewności | confidence score | Wartość opisująca wiarygodność wyniku algorytmu, jeśli narzędzie ją udostępnia. |
| częstotliwość próbkowania | sample rate | Liczba próbek sygnału audio zapisywanych w ciągu sekundy. |
| modulacja kodowo-impulsowa | Pulse-Code Modulation, PCM | Standardowa reprezentacja próbek cyfrowego audio. |
| synchronizacja ruchu ust z mową | lip-sync | W tytułach można zachować „lip-sync” po polskim rozwinięciu. |
| żuchwa | jaw/mandible | Dla anatomii preferować mandible, dla kanału sterującego jaw. |
| domknięcie warg | lip seal | |

## Capture, fotogrametria i rekonstrukcja

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| pozyskiwanie materiału referencyjnego | reference capture | |
| sesja zdjęciowa do rekonstrukcji | photogrammetry capture | |
| fotogrametria | photogrammetry | |
| parametry wewnętrzne aparatu | camera intrinsics | Parametry modelu kamery, m.in. ogniskowa w pikselach i punkt główny. |
| zniekształcenie promieniowe | radial distortion | Zniekształcenie obrazu rosnące zwykle wraz z odległością od środka kadru. |
| balans bieli | white balance | Ustawienie określające neutralne odwzorowanie barw dla danego oświetlenia. |
| rekonstrukcja z ruchu kamery | Structure from Motion, SfM | Pełna polska nazwa + nazwa standardowa. |
| wielowidokowa rekonstrukcja stereo | Multi-View Stereo, MVS | |
| dopasowanie cech | feature matching | |
| punkt charakterystyczny | feature point | |
| błąd reprojekcji | reprojection error | |
| maska pierwszego planu | foreground mask | |
| segmentacja pierwszego planu | foreground segmentation | |
| rekonstrukcja obiektocentryczna | object-centric reconstruction | |
| osoba obracająca się przed kamerą | rotating-subject capture | Nazwa procesu self-capture. |

## Czas rzeczywisty i eksport

| Polski termin | Angielski termin | Uwagi |
| --- | --- | --- |
| środowisko czasu rzeczywistego | runtime environment | W skrócie „środowisko czasu rzeczywistego”, nie samo „runtime” w tekście dydaktycznym. |
| środowisko docelowe | target environment | |
| wersja wzorcowa | master asset | Oznacza źródłowy artefakt najwyższej jakości. |
| artefakt pochodny | derived artifact | |
| profil eksportu | export profile | |
| format pośredni | interchange format | |
| wywołanie wsadowe | batch invocation | |
| interfejs wiersza poleceń | command-line interface, CLI | |

## Rozstrzyganie nowych terminów

Przy dodawaniu terminu, którego nie ma w słowniku:

1. sprawdź polskie normy, podręczniki akademickie, dokumentację uczelni lub polską dokumentację producenta;
2. wybierz termin opisująjący znaczenie, a nie mechaniczną kalkę słowo po słowie;
3. dodaj angielski odpowiednik w nawiasie;
4. wpisz termin do tego słownika przed użyciem go w wielu dokumentach;
5. przy pierwszym użyciu przygotuj dydaktyczne wyjaśnienie zgodne z zasadą pierwszego użycia pojęcia;
6. nie zmieniaj istniejących identyfikatorów API, formatów danych ani nazw wymaganych przez standardy.

W razie kilku poprawnych polskich odpowiedników preferujemy formę najbardziej jednoznaczną w grafice komputerowej, optyce, animacji lub informatyce.