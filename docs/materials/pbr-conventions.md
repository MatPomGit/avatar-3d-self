# Konwencje renderowania opartego na fizyce

Avatar Studio używa **modelu metaliczności i chropowatości (metallic-roughness workflow)** jako kanonicznego interfejsu dla **renderowania opartego na fizyce (Physically Based Rendering, PBR)**. Wersja wzorcowa zasobu (master asset) może przechowywać więcej informacji niż środowisko czasu rzeczywistego (runtime environment), ale eksport nie może zmieniać fizycznego znaczenia map.

Terminologia w tym rozdziale jest zgodna ze [słownikiem terminologicznym](../project/terminology.md).

## Kanoniczne mapy materiałowe

- **barwa bazowa (Base Color)** lub albedo: przestrzeń sRGB, bez wypalonego oświetlenia;
- **mapa normalnych (normal map)**: dane liniowe (linear data), z jawną konwencją osi Y;
- **mapa chropowatości (roughness map)**: dane liniowe;
- **mapa metaliczności (metallic map)**: dane liniowe i tylko dla rzeczywistych materiałów metalicznych;
- **mapa okluzji otoczenia (Ambient Occlusion map, AO)**: dane liniowe, używana pomocniczo;
- **mapa wysokości (height map)** lub **mapa przemieszczeń (displacement map)**: dane liniowe, gdy uzasadnia to geometria i środowisko docelowe (target environment);
- **mapa przezroczystości (opacity map)** lub kanał alfa (alpha channel): dane liniowe;
- **mapa emisji (emissive map)**: przestrzeń barw (color space) zgodna z profilem środowiska docelowego;
- maska **rozpraszania podpowierzchniowego (Subsurface Scattering, SSS)**: dane liniowe.

## Zakresy wartości

Mapy skalarne przechowujemy w zakresie 0-1, o ile format źródłowy lub zjawisko fizyczne nie wymaga innej reprezentacji. Nie obcinamy danych tylko po to, aby wyglądały poprawnie w jednym programie cieniującym (shader).

### Metaliczność (metallic)

- skóra, włosy, tkaniny, oczy i szkło: `0`;
- czyste metale w modelu metaliczności: `1`;
- materiały warstwowe lub mieszane opisujemy odpowiednią maską, a nie przypadkową wartością pośrednią.

Nie zwiększamy metaliczności (metallic) w celu uzyskania silniejszego refleksu dielektryka.

### Chropowatość (roughness)

Chropowatość (roughness) opisuje statystyczną mikrogeometrię powierzchni wpływającą na rozkład odbicia. Nie jest jasnością refleksu ani zamiennikiem ekspozycji.

Nie wolno:

- malować cieni do mapy chropowatości (roughness map);
- używać chropowatości (roughness) do kompensowania błędnego oświetlenia;
- nadawać całej skórze lub tkaninie jednej wartości, jeśli materiał referencyjny wykazuje lokalną zmienność.

## Współczynnik załamania i odbicie Fresnela

Dla dielektryka **współczynnik odbicia Fresnela dla padania prostopadłego (normal-incidence Fresnel reflectance, F0)** można obliczyć ze **współczynnika załamania światła (Index of Refraction, IOR)**:

`F0 = ((IOR - 1) / (IOR + 1))^2`

Przykładowo dla `IOR = 1.5` otrzymujemy `F0 ≈ 0.04`.

Jeżeli środowisko docelowe (target environment) obsługuje współczynnik załamania światła (IOR) bezpośrednio, przechowujemy tę wartość. Jeżeli model materiałowy używa współczynnika F0, konwersja musi być jawna i odtwarzalna.

## Mapa normalnych (normal map)

Wersja wzorcowa (master asset) przechowuje mapę normalnych w przestrzeni stycznej (tangent-space normal map) z udokumentowaną konwencją osi Y.

Baseline:

- brak kompresji stratnej (lossy compression) w wersji wzorcowej;
- **głębia bitowa (bit depth)** 16 bitów na kanał, gdy źródło zawiera subtelne dane pochodzące z mapy przemieszczeń (displacement map);
- środowisko czasu rzeczywistego (runtime environment) może używać kompresji BC5 lub równoważnej;
- konwersja konwencji OpenGL i DirectX wymaga odwrócenia składowej Y i musi być wykonywana automatycznie przez profil eksportu (export profile).

## Mapa wysokości i mapa przemieszczeń

Wersja wzorcowa mapy przemieszczeń (displacement map) musi zachowywać skalę fizyczną. Jeżeli wartości są znormalizowane, metadane przechowują co najmniej:

- poziom odniesienia `midlevel`;
- skalę w milimetrach `scale_mm`;
- jednostkę długości.

Bez tych danych mapa przemieszczeń (displacement map) nie jest samodzielnym i odtwarzalnym artefaktem.

## System kafli tekstur UDIM

Dla poziomu szczegółowości LOD0 dopuszczamy **system kafli tekstur UDIM (UDIM texture tiling)**.

Baseline:

- twarz i uszy: własny kafel UDIM (UDIM tile) lub zestaw kafli;
- tułów: osobny kafel;
- kończyny: osobne kafle zależnie od potrzeb;
- dłonie mogą mieć większą gęstość tekseli (texel density);
- symetria rozwinięcia UV (UV unwrapping) nie jest wymagana, ponieważ cechy skóry i ubrań są asymetryczne.

## Gęstość tekseli (texel density)

Dla tekstury 4K w wersji wzorcowej przyjmujemy efektywną gęstość tekseli (texel density):

- twarz: 20-30 px/cm;
- dłonie: 15-25 px/cm;
- ciało: 8-16 px/cm;
- ubrania: 8-16 px/cm;
- okulary i małe akcesoria: zwykle 10-20 px/cm, zależnie od odległości kamery.

Nie trzeba zachowywać identycznej gęstości tekseli (texel density) dla wszystkich części. Priorytetem jest percepcyjna ważność obszaru i przewidywana odległość kamery.

## Margines między wyspami UV (UV padding)

Dla tekstur 4K:

- minimum: 8 px;
- wartość bazowa: 16 px;
- preferowane: 24-32 px dla zasobów intensywnie korzystających z łańcucha mipmap (mipmap chain).

Margines między wyspami UV (UV padding) musi uwzględniać kolejne poziomy łańcucha mipmap (mipmap chain), aby uniknąć przenikania barw między wyspami.

## Głębia bitowa (bit depth)

Dla wersji wzorcowej:

- barwa bazowa (Base Color): 16 bitów na kanał w TIFF, PNG lub EXR, jeśli dane źródłowe mają taką użyteczną precyzję;
- mapa chropowatości (roughness map): preferowane 16 bitów podczas tworzenia;
- mapa normalnych (normal map): preferowane 16 bitów dla wzorcowego wypalania tekstur (texture baking);
- mapa przemieszczeń (displacement map): minimum 16 bitów, preferowane 32-bitowe wartości zmiennoprzecinkowe (32-bit floating point) dla precyzyjnej wersji wzorcowej;
- środowisko czasu rzeczywistego (runtime environment): format i kompresja zależne od silnika.

JPEG nie jest formatem źródłowym dla mapy chropowatości (roughness map), mapy normalnych (normal map) ani mapy przemieszczeń (displacement map).

## Przestrzeń barw (color space)

- barwa bazowa (Base Color) i typowa mapa emisji (emissive map): sRGB, o ile profil środowiska docelowego nie stanowi inaczej;
- mapa normalnych (normal map), mapa chropowatości (roughness map), mapa metaliczności (metallic map), mapa okluzji otoczenia (AO) oraz mapa wysokości (height map): dane liniowe (linear data);
- każda automatyczna konwersja przestrzeni barw (color space) musi być jawna w raporcie eksportu.

Nie wolno oznaczać map danych jako sRGB tylko dlatego, że są zapisane w formacie PNG.

## Nazewnictwo

Stosujemy wzorzec:

`asset_material_map_resolution_vNNN.ext`

Przykład dla mapy chropowatości (roughness map):

`head_skin_roughness_4k_v003.png`

Przykład dla systemu kafli tekstur UDIM (UDIM texture tiling):

`head_skin_basecolor_1001_4k_v003.exr`

Nazwy pól i plików zachowują angielskie identyfikatory, ponieważ są częścią kontraktu technicznego.

## Profil środowiska docelowego

Wersja wzorcowa materiału pozostaje neutralna wobec silnika. Konwersje do Unreal Engine, Unity i środowiska webowego są profilami eksportu (export profiles).

Profil zapisuje co najmniej:

- sposób pakowania kanałów (channel packing);
- konwencję osi Y mapy normalnych (normal map Y convention);
- format kompresji (compression format);
- przestrzeń barw (color space);
- maksymalny rozmiar tekstury (maximum texture size);
- model rozpraszania podpowierzchniowego (SSS model);
- szablon i wersję programu cieniującego (shader template/version).

## Walidacja

Każdy materiał sprawdzamy w:

1. neutralnym świetle studyjnym;
2. świetle bocznym;
3. oświetleniu od tyłu (backlight);
4. wysokim kontraście;
5. neutralnym szarym środowisku HDRI lub równoważnym środowisku referencyjnym.

Materiał zalicza etap, jeśli:

- nie zależy od jednego środowiska HDRI;
- mapy mają poprawnie przypisaną przestrzeń barw (color space);
- nie ma widocznych szwów UV (UV seams) na kolejnych poziomach łańcucha mipmap (mipmap chain);
- spakowane kanały (packed channels) są zgodne z profilem środowiska docelowego;
- skala mapy przemieszczeń (displacement map) jest odtwarzalna;
- nazwy i wersje są jednoznaczne.

Szczegółowe zasady układu UV i tekstur opisuje dokument [Rozwinięcie UV i układ tekstur](uv-texture-layout.md).