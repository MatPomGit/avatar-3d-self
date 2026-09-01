# PBR conventions

Avatar Studio używa metal/roughness workflow jako kanonicznego interfejsu materiałowego. Master może przechowywać dane bogatsze niż target runtime, ale eksport nie może zmieniać znaczenia map.

## Mapy

- Base Color / Albedo: sRGB, bez wypalonego oświetlenia;
- Normal: linear, zgodna konwencja osi Y dla targetu;
- Roughness: linear;
- Metallic: linear i tylko dla rzeczywistych materiałów metalicznych;
- Ambient Occlusion: linear, pomocniczo;
- Height / Displacement: linear, gdy uzasadnione gęstością geometrii i targetem;
- Opacity/Alpha: linear;
- Emissive: sRGB lub zgodnie z targetem;
- SSS/scatter mask: linear.

## Zakresy wartości

Wszystkie mapy skalarskie są przechowywane w zakresie 0-1. Nie clipujemy danych źródłowych tylko po to, aby „wyglądały dobrze” w pojedynczym rendererze.

### Metallic

- skóra, włosy, tkaniny, oczy, szkło: `0`;
- czyste metale: `1`;
- materiały mieszane używają maski obszarów, a nie wartości pośredniej jako substytutu połysku.

Wartości 0.1-0.9 są dozwolone wyłącznie na granicach filtrowania lub tam, gdzie materiał rzeczywiście jest mieszaniną warstw opisaną przez target shader.

### Roughness

Roughness jest liniowa i opisuje mikroskopijną chropowatość, nie jasność highlightu.

Nie wolno:

- malować cieni do roughness;
- używać roughness do kompensowania błędnego oświetlenia;
- ustawiać jednej wartości dla całej skóry lub ubrania, jeśli referencja wykazuje lokalną zmienność.

## Fresnel i IOR

Dla dielektryka podstawowe F0 można wyznaczyć z IOR:

`F0 = ((IOR - 1) / (IOR + 1))^2`

Przykładowo dla `IOR = 1.5`, `F0 ≈ 0.04`.

Jeśli target shader obsługuje IOR bezpośrednio, zapisujemy IOR. Jeśli używa klasycznego specular/F0, konwersja musi być jawna w exporterze.

Nie zwiększamy metallic w celu uzyskania silniejszego refleksu dielektryka.

## Normal maps

Kanoniczny master przechowuje tangent-space normal z udokumentowaną konwencją osi Y.

Baseline:

- brak kompresji stratnej w master;
- 16-bit, jeśli pipeline generuje subtelne dane displacement-derived;
- runtime może używać 8-bit BC5 lub odpowiednika;
- konwersja OpenGL ↔ DirectX wymaga odwrócenia kanału Y i musi być wykonywana automatycznie przez profil eksportu.

## Height i displacement

Displacement master powinien zachować skalę fizyczną. Jeśli mapa jest znormalizowana, metadata musi zawierać:

- `midlevel`;
- `scale_mm`;
- jednostkę.

Bez tych danych mapa displacement nie jest samodzielnym artefaktem reprodukowalnym.

## UDIM

Dla LOD0 dopuszczamy UDIM.

Baseline:

- twarz i uszy: własny tile lub zestaw tile;
- tułów: osobny tile;
- kończyny: osobne tile zależnie od potrzeb;
- dłonie mogą mieć zwiększoną texel density;
- symetria UV nie jest wymagana, ponieważ cechy skóry i ubrań są asymetryczne.

## Texel density

Dla master 4K przyjmujemy baseline efektywnej gęstości:

- twarz: 20-30 px/cm;
- dłonie: 15-25 px/cm;
- ciało: 8-16 px/cm;
- ubrania: 8-16 px/cm;
- okulary i małe akcesoria: zależnie od odległości kamery, zwykle 10-20 px/cm.

Nie trzeba zachowywać identycznej gęstości dla wszystkich części. Priorytetem jest percepcyjna ważność obszaru.

## Padding

Dla tekstur 4K:

- minimum: 8 px;
- baseline: 16 px;
- preferowane 24-32 px dla assetów intensywnie mipmapowanych.

Padding musi uwzględniać mip chain.

## Bit depth

Master:

- Base Color: 16-bit TIFF/PNG/EXR, jeśli źródło ma użyteczną głębię;
- Roughness: 16-bit preferowane podczas authoringu;
- Normal: 16-bit preferowane dla bake master;
- displacement: 16-bit minimum, 32-bit float dla precyzyjnego master;
- runtime: kompresja zależna od silnika.

Nie przechowujemy JPEG jako źródłowej roughness, normal ani displacement.

## Nazewnictwo

Stosuj wzorzec:

`asset_material_map_resolution_vNNN.ext`

Przykład:

`head_skin_roughness_4k_v003.png`

Dla UDIM:

`head_skin_basecolor_1001_4k_v003.exr`

## Profile targetów

Master materiałowy jest neutralny wobec silnika. Konwersje do Unreal, Unity i Web są profilami eksportu.

Profil zapisuje co najmniej:

- kanały packed maps;
- normal Y convention;
- compression format;
- color space;
- max texture size;
- SSS model;
- shader template/version.

## Walidacja

Każdy materiał sprawdź w:

1. neutralnym świetle studyjnym;
2. świetle bocznym;
3. backlight;
4. wysokim kontraście;
5. neutralnym szarym HDRI lub równoważnym środowisku referencyjnym.

Materiał zalicza etap, jeśli:

- nie zależy od jednego HDRI;
- mapy mają poprawne color space;
- nie ma szwów UV w mipach;
- packed channels są zgodne z profilem targetu;
- skala displacement jest odtwarzalna;
- nazwy i wersje są jednoznaczne.
