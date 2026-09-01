# ADR-0006: Avatar Studio jako kanoniczna nazwa produktu

## Status

Accepted.

## Kontekst

Projekt rozwinął się z repozytorium poświęconego pojedynczemu awatarowi do kompletnego środowiska obejmującego dokumentację produkcyjną, walidatory, integracje z narzędziami DCC oraz aplikację desktopową prowadzącą użytkownika przez cały pipeline. Nazwa repozytorium została już administracyjnie ujednolicona z nazwą produktu.

## Decyzja

Kanoniczna nazwa produktu to **Avatar Studio**, a kanoniczne repozytorium GitHub to `MatPomGit/avatar-studio`.

Stosujemy następujące identyfikatory:

- produkt i UI: `Avatar Studio`;
- repozytorium GitHub: `MatPomGit/avatar-studio`;
- moduł/import Python: `avatar_studio`;
- dystrybucja Python i komenda CLI: `avatar-studio`;
- executable: `AvatarStudio.exe` na Windows i `AvatarStudio` na Linux;
- stan lokalny projektu: `.avatar-studio/`;
- dokumentacja publiczna: `https://matpomgit.github.io/avatar-studio/`.

## Konsekwencje

Kod, dokumentacja, konfiguracja MkDocs, instrukcje klonowania, odnośniki aplikacji desktopowej i automatyzacja mają używać wyłącznie kanonicznej nazwy repozytorium. Nazwa projektu Unreal Engine nie może być wyprowadzana z nazwy repozytorium. Skrypty integracyjne mają przyjmować ścieżkę do pliku `.uproject` lub wykrywać ją na podstawie zawartości katalogu projektu, dzięki czemu przyszłe zmiany nazwy repozytorium nie wpływają na eksport.
