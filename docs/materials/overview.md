# Materiały

Materiały Avatar Studio wykorzystują renderowanie oparte na fizyce (Physically Based Rendering, PBR). Każdy zasób ma jawnie określony model materiałowy, przestrzeń barw (color space), rozdzielczość oraz profil eksportu.

Zalecana kolejność lektury:

1. [Konwencje PBR](pbr-conventions.md);
2. [Rozwinięcie UV i układ tekstur](uv-texture-layout.md);
3. [Skóra](skin.md);
4. [Oczy](eyes.md);
5. [Włosy i zarost](hair.md);
6. [Ubrania](clothing.md);
7. [Okulary](glasses.md).

Materiały są zależne od poprawnego rozwinięcia UV i nie powinny utrwalać błędów geometrii. Barwa bazowa, mapa normalnych i mapa przemieszczeń reprezentują różne klasy informacji i nie mogą być używane zamiennie.
