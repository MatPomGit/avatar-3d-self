# Rozwinięcie UV i układ tekstur

Celem tego etapu jest przygotowanie rozwinięcia UV (UV unwrapping), które zachowuje skalę detalu, minimalizuje widoczność szwów i pozostaje stabilne dla wypalania tekstur (texture baking), malowania oraz eksportu do środowiska czasu rzeczywistego (runtime environment).

Terminologia jest zgodna ze [słownikiem terminologicznym](../project/terminology.md).

## Założenia

Rozwinięcie UV nie jest tylko sposobem „zmieszczenia modelu w kwadracie”. Jest częścią kontraktu między geometrią, materiałami, poziomami szczegółowości (Levels of Detail, LOD) i narzędziami eksportowymi.

Po zatwierdzeniu rozwinięcia UV jego zmiana wymaga ponownego sprawdzenia wszystkich tekstur i map wypalanych (baked maps).

## Planowanie szwów UV

Szew UV (UV seam) powinien znajdować się tam, gdzie:

- jest naturalnie ukryty przez anatomię, ubranie, włosy lub zmianę materiału;
- powierzchnia zmienia kierunek na tyle mocno, że jedna wyspa UV (UV island) generowałaby duże rozciągnięcie;
- rozdzielenie ułatwia zachowanie gęstości tekseli (texel density).

Dla twarzy nie prowadzimy szwu przez policzek, czoło, nos, czerwień wargową ani inne obszary często widoczne na zbliżeniach. Preferowane miejsca to tylna część głowy, granica skóry głowy, wewnętrzna strona ucha i obszary zasłonięte przez fryzurę.

## Gęstość tekseli

Gęstość tekseli (texel density) definiujemy jako liczbę elementów tekstury przypadających na jednostkę długości powierzchni modelu. Dla projektu przyjmujemy jednostkę `px/cm`.

Wartości bazowe dla wersji wzorcowej:

| Obszar | Gęstość tekseli (texel density) |
| --- | ---: |
| twarz | 20-30 px/cm |
| dłonie | 15-25 px/cm |
| ciało | 8-16 px/cm |
| ubrania | 8-16 px/cm |
| okulary i drobne akcesoria | 10-20 px/cm |

Twarz i dłonie mają celowo większą gęstość tekseli (texel density), ponieważ zawierają cechy istotne dla podobieństwa i są oglądane z bliska.

## System kafli tekstur UDIM

System kafli tekstur UDIM (UDIM texture tiling) jest preferowany dla wzorcowej wersji LOD0, gdy pojedyncza tekstura nie zapewnia wymaganej rozdzielczości.

Proponowany podział:

- `1001`: twarz i uszy;
- `1002`: skóra głowy i szyja;
- `1003`: tułów;
- `1004`: lewa kończyna górna;
- `1005`: prawa kończyna górna;
- `1006`: lewa kończyna dolna;
- `1007`: prawa kończyna dolna;
- `1008`: dłonie, jeżeli wymagają osobnego kafla.

Jest to układ bazowy. Można go zmienić, jeżeli pomiar gęstości tekseli (texel density) lub wymagania środowiska docelowego (target environment) wskazują lepszy podział.

## Margines między wyspami UV

Margines między wyspami UV (UV padding) musi uwzględniać łańcuch mipmap (mipmap chain). Dla tekstury 4K przyjmujemy:

- minimum 8 px;
- wartość bazową 16 px;
- 24-32 px dla zasobów intensywnie redukowanych przez kolejne poziomy mipmap.

Podczas wypalania tekstur (texture baking) stosujemy również margines wypalania (bake padding), który rozszerza poprawne dane poza granice wyspy UV (UV island). Margines wypalania nie zastępuje fizycznej odległości między wyspami.

## Zniekształcenie rozwinięcia

Po rozwinięciu UV sprawdzamy:

- rozciągnięcie powierzchni (UV stretch);
- lokalną zmianę skali;
- niezamierzone nakładanie wysp UV (UV overlap);
- kierunek ważnych struktur, np. splotu tkaniny;
- ciągłość cech na granicach wysp.

Dla twarzy nie akceptujemy widocznego rozciągnięcia w okolicy oczu, ust, nosa i uszu. Jeżeli korekta wymaga przesunięcia szwu, wykonujemy ją przed rozpoczęciem właściwego malowania tekstur.

## Nakładanie i symetria

Nakładanie wysp UV (UV overlap) jest zabronione dla unikalnej skóry twarzy, dłoni i innych obszarów zawierających asymetryczne cechy identyfikujące osobę.

Nakładanie może być dopuszczone dla powtarzalnych, nieidentyfikujących elementów technicznych, jeżeli:

- obie powierzchnie rzeczywiście mają identyczny materiał;
- nie będą otrzymywać indywidualnych zabrudzeń, zużycia ani znaków;
- nie utrudnia to wypalania tekstur (texture baking).

## Głębia bitowa i formaty robocze

Głębia bitowa (bit depth) zależy od typu danych:

- barwa bazowa (Base Color): 16 bitów na kanał, jeśli materiał źródłowy uzasadnia tę precyzję;
- mapa normalnych (normal map): 16 bitów w wersji wzorcowej;
- mapa chropowatości (roughness map): 16 bitów podczas tworzenia;
- mapa przemieszczeń (displacement map): minimum 16 bitów, preferowane 32-bitowe dane zmiennoprzecinkowe (32-bit floating point) dla wzorca.

Nie zwiększamy głębi bitowej (bit depth) sztucznie po utracie informacji w źródle. Konwersja obrazu 8-bitowego do 16-bitowego nie odtwarza brakującej precyzji.

## Przestrzeń barw

Przestrzeń barw (color space) i funkcja przenoszenia (transfer function) muszą odpowiadać znaczeniu mapy:

- barwa bazowa (Base Color): typowo sRGB;
- mapa normalnych (normal map), mapa chropowatości (roughness map), mapa metaliczności (metallic map), mapa okluzji otoczenia (AO) i mapa przemieszczeń (displacement map): dane liniowe (linear data).

Błędne oznaczenie mapy danych jako sRGB zmienia wartości liczbowe i może prowadzić do widocznych błędów materiału.

## Kontrola przed zatwierdzeniem

Rozwinięcie UV jest gotowe, jeżeli:

- nie ma niezamierzonego nakładania wysp UV;
- gęstość tekseli (texel density) mieści się w zatwierdzonym zakresie;
- wyspy mają wystarczający margines między wyspami UV (UV padding);
- szwy UV są umieszczone poza najważniejszymi obszarami percepcyjnymi;
- nie występuje istotne rozciągnięcie na twarzy i dłoniach;
- numeracja kafli UDIM (UDIM tiles) jest stabilna i zapisana w manifeście zasobu;
- wszystkie mapy mają prawidłową przestrzeń barw (color space) oraz głębię bitową (bit depth).

Po zatwierdzeniu rozwinięcie UV staje się częścią zamrożonego kontraktu produkcyjnego podobnie jak topologia.