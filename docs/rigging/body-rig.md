# Body rig

Body rig implementuje [canonical skeleton](skeleton-specification.md) oraz warstwę kontrolerów animatora.

## Minimalny zakres

Root, pelvis, spine, chest, neck, head, clavicles, arms, forearms, hands, thighs, calves, feet i toes. W miejscach dużego skrętu stosuj twist bones lub równoważny mechanizm rozpraszania rotacji.

## IK/FK

Kończyny powinny wspierać IK/FK z kontrolowanym przełączaniem bez skoku. Stopy potrzebują funkcjonalnego foot roll, a ręce stabilnego pole vector.

Rig kontrolny i deformacyjny powinny być logicznie rozdzielone, jeśli narzędzie DCC na to pozwala.