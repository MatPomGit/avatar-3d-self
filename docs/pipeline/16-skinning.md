# 16. Skinning i deformacja

**Input:** kompletna geometria i rig.  
**Editable output:** zatwierdzone weights + corrective shapes.  
**Gate:** deformation approval.

## Windows

1. Rozpocznij od automatycznych wag tylko jako punktu startowego.
2. Normalizuj influences i ogranicz je zgodnie z target engine.
3. Ręcznie popraw shoulder, elbow, wrist, fingers, hip, knee, ankle i neck.
4. Dodaj correctives tam, gdzie sama interpolacja kości nie zachowuje objętości.
5. Uruchom pełny pose test matrix.

## Linux

1. Wykonaj skinning na tej samej zamrożonej topologii.
2. Sprawdź distribution weights i zero-weight vertices.
3. Popraw regiony o dużej zmianie objętości.
4. Zweryfikuj ubrania oddzielnie od skóry.
5. Zapisz wyniki testów deformacji.

## DoD

Brak widocznych implozji, ostrych fałd technicznych, odrywających się ubrań i niekontrolowanych influences. Test matrix ma status passed.
