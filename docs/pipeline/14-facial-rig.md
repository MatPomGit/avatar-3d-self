# 14. Rig twarzy

**Input:** zamrożona topologia twarzy, expression capture i oczy.  
**Editable output:** jaw/eyes controls + blend shapes/bones.  
**Specification:** [Facial rig specification](../rigging/facial-rig-specification.md).

## Windows

1. Utwórz osobną żuchwę i poprawny pivot w stawie skroniowo-żuchwowym.
2. Powiąż dolne zęby i odpowiednią część języka z jaw motion.
3. Zbuduj kanoniczny zestaw ARKit coefficients.
4. Zachowaj niezależność lewej/prawej strony dla asymetrycznych shapes.
5. Dodaj eye aim, blink, eyelid follow i cheek interaction.

## Linux

1. Zbuduj jaw i oral cavity controls.
2. Odtwórz shapes na podstawie expression capture, nie z abstrakcyjnego template'u.
3. Zmapuj shapes do ARKit i FACS.
4. Dodaj corrective shapes dla konfliktowych ekspresji.
5. Wykonaj test mieszanek, nie tylko pojedynczych shapes.

## DoD

Pełny wymagany zestaw shapes działa pojedynczo i w kombinacjach, jaw ma anatomiczny ruch, blink jest szczelny, a twarz zachowuje podobieństwo przy ekspresji.
