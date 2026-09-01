# Kanoniczna specyfikacja skeletonu

Nazwy są kontraktem między Blenderem, exporterem, Avatar Studio i target engine.

## Rdzeń

```text
root
└── pelvis
    ├── spine_01
    │   └── spine_02
    │       └── spine_03
    │           └── neck_01
    │               └── head
    ├── thigh_l → calf_l → foot_l → ball_l
    └── thigh_r → calf_r → foot_r → ball_r
```

Ramiona od `spine_03`:

```text
clavicle_l → upperarm_l → lowerarm_l → hand_l
clavicle_r → upperarm_r → lowerarm_r → hand_r
```

## Dłonie

Dla każdej strony:

```text
thumb_01 → thumb_02 → thumb_03
index_01 → index_02 → index_03
middle_01 → middle_02 → middle_03
ring_01 → ring_02 → ring_03
pinky_01 → pinky_02 → pinky_03
```

Metacarpals mogą być dodane, jeśli poprawiają spread/cupping i docelowy retargeter je obsługuje. Twist bones (`upperarm_twist`, `lowerarm_twist`, `thigh_twist`) są zalecane po wykazaniu korzyści w deformation tests.

## Zasady

- `root` odpowiada za globalny transform/root motion.
- deform bones są oddzielone od controllers.
- osie lokalne muszą być spójne między stronami.
- skala rest skeletonu wynika z rzeczywistej anatomii postaci.
- A-pose jest preferowaną rest pose projektu, chyba że target rig wymaga inaczej.

## Windows

W Blenderze zapisuj skeleton w kanonicznej scenie `.blend`; eksportuj profile FBX dopiero po przejściu testu nazw i axes.

## Linux

Stosuj tę samą scenę i nazwy. Blender CLI może służyć do automatycznej walidacji hierarchy, ale nie zmienia specyfikacji.
