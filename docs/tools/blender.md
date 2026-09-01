# Blender

Blender jest kanonicznym DCC projektu. Wersję używaną do zatwierdzonego artefaktu zapisuj w raporcie.

## Windows

Po instalacji sprawdź CLI:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.x\blender.exe" --version
```

W Avatar Studio zapisz rzeczywistą ścieżkę `blender.exe`. Do automatycznych walidacji używaj `--background --python <script>` i zapisuj stdout/stderr.

## Linux

```bash
blender --version
which blender
```

Jeżeli używasz wersji portable, skonfiguruj jej pełną ścieżkę w Avatar Studio. Skrypty walidacyjne nie powinny zakładać konkretnego katalogu instalacji.
