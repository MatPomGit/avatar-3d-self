# PBR conventions

## Mapy

- Base Color / Albedo: sRGB, bez wypalonego oświetlenia;
- Normal: linear, zgodna konwencja osi Y dla targetu;
- Roughness: linear;
- Metallic: linear i tylko dla materiałów metalicznych;
- Ambient Occlusion: linear, pomocniczo;
- Height / Displacement: linear, gdy uzasadnione gęstością geometrii i targetem.

## Nazewnictwo

Stosuj wzorzec `asset_material_map_resolution_vNNN.ext`, np. `head_skin_roughness_4k_v003.png`.

## Walidacja

Każdy materiał sprawdź w neutralnym świetle studyjnym, świetle bocznym i wysokim kontraście. Jeśli detal znika bez konkretnego HDRI, prawdopodobnie został zakodowany w niewłaściwej mapie.