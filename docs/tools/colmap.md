# COLMAP

COLMAP jest narzędziem rekonstrukcji, nie elementem zależności pakietu Python.

## Windows

1. Zainstaluj oficjalny build COLMAP.
2. W terminalu sprawdź dostępność `colmap.exe` albo wskaż pełną ścieżkę w Avatar Studio.
3. Wykonuj rekonstrukcję w prywatnym workspace.
4. Zapisuj database, sparse model i parametry wraz z raportem sesji.

Przykład diagnostyki:

```powershell
colmap.exe -h
```

## Linux

1. Zainstaluj COLMAP z repozytorium dystrybucji lub oficjalnego builda.
2. Sprawdź:

```bash
colmap -h
which colmap
```

3. Używaj prywatnego workspace i zapisuj wersję programu w raporcie.
4. Nie uruchamiaj dużej rekonstrukcji w CI.
