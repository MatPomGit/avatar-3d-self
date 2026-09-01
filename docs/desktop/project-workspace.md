# Workspace projektu Avatar Studio

Avatar Studio działa na lokalnym katalogu roboczym użytkownika. Katalog może znajdować się poza repozytorium i może zawierać prywatne zdjęcia, modele oraz nagrania.

## Struktura logiczna

```text
my-avatar/
├── references/
├── source/
├── textures/
├── animations/
├── exports/
├── reports/
└── .avatar-studio/
    └── project.sqlite3
```

Nazwy katalogów użytkownika nie muszą być identyczne, ale aplikacja powinna przechowywać ich role w ustawieniach projektu.

## `.avatar-studio/`

Katalog jest technicznym stanem projektu. Zawiera bazę SQLite, a docelowo również logi uruchomień narzędzi i cache bezpieczny do odtworzenia. Nie powinien zawierać kopii dużych zdjęć, skanów ani modeli, jeśli nie jest to konieczne.

## Zasada źródła prawdy

Pliki DCC i artefakty pozostają plikami na dysku. SQLite przechowuje ich ścieżki, hash, role, metadane i wyniki walidacji. Baza danych nie zastępuje źródłowej sceny Blender ani innych plików produkcyjnych.

## Przenoszenie projektu

Przy zmianie komputera należy przenieść workspace wraz z `.avatar-studio/`. Jeśli zmienią się ścieżki bezwzględne, aplikacja powinna umożliwić ponowne wskazanie root workspace i relokację artefaktów na podstawie ścieżek względnych oraz SHA-256.

## Prywatność

Workspace może zawierać dane biometryczne. Nie zakładaj synchronizacji z chmurą. Funkcja eksportu projektu powinna oddzielać publiczne raporty i manifesty od prywatnych źródeł.