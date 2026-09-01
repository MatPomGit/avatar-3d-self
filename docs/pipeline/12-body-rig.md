# 12. Rig ciała

**Input:** zatwierdzony base mesh.  
**Editable output:** skeleton + control rig w scenie DCC.  
**Specification:** [Skeleton specification](../rigging/skeleton-specification.md).

## Windows

1. Umieść `root`, pelvis, spine, neck i head zgodnie z anatomią.
2. Dodaj clavicle, limbs, feet i twist bones.
3. Zdefiniuj lokalne osie konsekwentnie dla lewej i prawej strony.
4. Dodaj IK/FK switching dla kończyn.
5. Nie używaj control bones jako deform bones bez jawnej potrzeby.

## Linux

1. Zbuduj skeleton według kanonicznej hierarchii.
2. Ustaw joint centers na podstawie anatomii i testów deformacji.
3. Dodaj twist distribution dla forearm/upper arm/thigh, jeśli jest potrzebny.
4. Skonfiguruj IK/FK i pole targets.
5. Zapisz rest pose jako niezmienny punkt odniesienia.

## DoD

Skeleton przechodzi test pełnego zakresu ruchu, osie są spójne, nazwy zgodne ze specyfikacją, a rest pose jest udokumentowana.
