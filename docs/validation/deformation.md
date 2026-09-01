# Walidacja deformacji

Skinning i correctives są zatwierdzane przez macierz póz, nie przez pojedynczą T/A-pose.

## Ciało

Minimalny zestaw:

- shoulder flexion 0°, 45°, 90°, 150°;
- shoulder abduction 0°, 45°, 90°, 150°;
- elbow 0°, 45°, 90°, 130°;
- forearm pronation/supination około ±80°;
- wrist flexion/extension około ±60°;
- hip flexion 0°, 45°, 90°, 120°;
- knee 0°, 45°, 90°, 130°;
- ankle dorsiflexion 20° i plantarflexion 35°.

Zakresy są testowe, nie medyczne limity postaci. Avatar nie musi osiągać pozy powodującej nienaturalne naprężenie referencyjnej anatomii.

## Dłonie

Pełna pięść, pinch, chwyt cylindryczny, wskazywanie i opozycja kciuka. Każdy palec testowany osobno. Nie akceptujemy zapadania knuckles ani utraty objętości opuszek.

## Twarz

Jaw open, smile, frown, pucker, funnel, blink, squint, brows oraz kombinacje. Krytyczne są okolice commissures, nasolabial fold, dolnej powieki i żuchwy.

## Tolerancja penetracji

Widoczna penetracja skóry, zębów, oka lub odzieży w kluczowej pozie to fail. Drobne kolizje <1 mm mogą być warning tylko w ekstremalnych pozach, których runtime nie używa.

## Correctives

Corrective shape jest wymagany, jeśli problem nie może być usunięty wagami bez pogorszenia sąsiednich póz. Corrective ma mieć jawny driver i test regresyjny.