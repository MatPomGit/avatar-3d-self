# Capture manifest

Manifest opisuje sesję bez konieczności publikowania zdjęć. Powinien zawierać wszystkie informacje potrzebne do odtworzenia sposobu wykonania materiału i oceny jego jakości.

## Minimalny manifest

```json
{
  "schema_version": 2,
  "session_id": "body-rotating-001",
  "capture_type": "photogrammetry",
  "capture_method": "rotating_subject",
  "device": "camera model",
  "lens": "main-1x",
  "focal_length_equivalent_mm": 55,
  "resolution": [6000, 4000],
  "lighting": "diffuse-fixed",
  "pose": "a-pose",
  "image_count": 108,
  "known_scale_mm": 1800.0,
  "scale_measurements": [
    {"name": "height", "value_mm": 1800.0},
    {"name": "shoulder_width", "value_mm": 460.0},
    {"name": "arm_span", "value_mm": 1810.0}
  ],
  "rotating_subject": {
    "angle_step_deg": 10.0,
    "positions_per_ring": 36,
    "camera_levels": 3,
    "settle_time_s": 2.0,
    "foreground_masks": true,
    "mask_dilation_px": 5,
    "reconstruction_mode": "object_centric"
  },
  "rejected_frames": [],
  "notes": [],
  "privacy": {"public": false}
}
```

## `capture_method`

Dozwolone podstawowe wartości:

- `moving_camera`: osoba pozostaje nieruchoma, kamera zmienia pozycję;
- `rotating_subject`: kamera pozostaje nieruchoma, osoba obraca całe ciało pomiędzy zdjęciami;
- `reference_only`: materiał służy do modelowania lub oceny, nie do photogrammetry solve;
- `expression_capture`: osobna seria ekspresji twarzy.

Wartość `turntable_masked` z wcześniejszych wersji dokumentacji jest zastąpiona przez bardziej ogólne `rotating_subject`. Migracja manifestu powinna zachować semantykę starego pola.

## Pola wariantu `rotating_subject`

Dla samodzielnego capture sylwetki wymagane są:

- `angle_step_deg`;
- `positions_per_ring`;
- `camera_levels`;
- `settle_time_s`;
- `foreground_masks`;
- `reconstruction_mode`.

Jeżeli `foreground_masks=false`, Avatar Studio powinno zgłosić ostrzeżenie wysokiego poziomu przed rekonstrukcją.

## Pomiary skali

`known_scale_mm` jest zachowane dla kompatybilności, ale preferowane jest `scale_measurements` z co najmniej trzema pomiarami całej sylwetki.

Dla ciała rekomendowane są:

- wzrost;
- szerokość barków;
- rozpiętość ramion;
- opcjonalnie długość nogi, obwód głowy lub długość dłoni.

Jeśli pomiary są niespójne z rekonstrukcją o więcej niż 1%, należy sprawdzić solve przed automatycznym skalowaniem.

## Odrzucone klatki

Każda odrzucona klatka może być opisana:

```json
{
  "file": "IMG_0042.CR3",
  "reason": "pose_drift",
  "replacement": "IMG_0042B.CR3"
}
```

Typowe `reason`:

- `motion_blur`;
- `pose_drift`;
- `hair_motion`;
- `clothing_motion`;
- `exposure_change`;
- `mask_error`;
- `occlusion`;
- `duplicate`.

## Prywatność

Nie zapisuj GPS, adresu ani danych kontaktowych, jeśli nie są technicznie konieczne. EXIF zawierający lokalizację powinien być usunięty z kopii przeznaczonych do współdzielenia.

## Windows

Przechowuj manifest obok prywatnej sesji, np.:

```text
D:\Avatar3D\projects\self-avatar\capture\body\capture_manifest.json
```

## Linux

Przechowuj go analogicznie:

```text
~/Avatar3D/projects/self-avatar/capture/body/capture_manifest.json
```

## Walidacja przez Avatar Studio

Przed rozpoczęciem rekonstrukcji aplikacja powinna sprawdzić:

1. `schema_version`;
2. kompletność wymaganych pól;
3. zgodność `image_count` z rzeczywistą liczbą plików;
4. dostępność masek dla `rotating_subject`;
5. dodatnią wartość pomiarów skali;
6. brak duplikatów nazw plików;
7. obecność informacji o odrzuconych klatkach;
8. zgodność kąta i liczby pozycji z pełnym pokryciem 360°.

Dla `rotating_subject` relacja kontrolna wynosi:

`coverage_deg = angle_step_deg * positions_per_ring`.

Baseline wymaga `coverage_deg >= 360°`.
