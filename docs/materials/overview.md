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

## Mapa decyzyjna

| Decyzja | Odpowiedź |
| --- | --- |
| Wymagane wejście | Mesh z zatwierdzoną topologią i skalą, zatwierdzone UV oraz skalibrowane referencje koloru i powierzchni. |
| Kolejność lektury | [Konwencje PBR](pbr-conventions.md) → [UV i układ tekstur](uv-texture-layout.md) → [skóra](skin.md) → [oczy](eyes.md) → [włosy](hair.md) → [ubrania](clothing.md) → [okulary](glasses.md). |
| Rezultat | Edytowalne tekstury i materiały PBR dla osobnych zasobów, z profilem eksportu i kontrolowanymi przestrzeniami barw. |
| Przejście dalej | Materiały przechodzą porównanie w referencyjnym oświetleniu, nie maskują błędów geometrii i zachowują się poprawnie po próbnym imporcie do docelowego runtime. |
| Gdy warunek nie jest spełniony | Nie kompensuj geometrii teksturą i nie zatwierdzaj eksportu. Ustal klasę problemu według [walidacji uncanny valley](../validation/uncanny-valley.md) i [diagnostyki aplikacji](../desktop/troubleshooting.md). |
