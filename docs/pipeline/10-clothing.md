# 10. Ubrania

**Input:** zatwierdzone ciało, zdjęcia i wymiary ubrań.  
**Editable output:** osobne modele ubrań z UV i materiałami.

## Windows

1. Modeluj ubrania jako oddzielną geometrię w rest pose.
2. Zachowaj realistyczną grubość i konstrukcję szwów tam, gdzie jest widoczna.
3. Przenieś bazowe skin weights z ciała i popraw regiony stawów.
4. Dodaj cloth simulation tylko dla elementów, które rzeczywiście jej wymagają.
5. Sprawdź penetration w pełnym zestawie test poses.

## Linux

1. Utwórz oddzielny mesh każdego elementu garderoby.
2. Przygotuj własne UV i PBR.
3. Dopasuj skinning do ciała.
4. Skonfiguruj kolizje lub uproszczoną dynamikę.
5. Przetestuj barki, łokcie, biodra, siad i chód.

## DoD

Ubrania nie zastępują powierzchni skóry, nie deformują się jak guma, zachowują sylwetkę materiału i nie generują krytycznych penetracji.
