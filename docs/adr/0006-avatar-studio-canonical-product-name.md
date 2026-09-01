# ADR-0006: Avatar Studio jako kanoniczna nazwa produktu

## Status

Accepted.

## Kontekst

Projekt rozwinął się z repozytorium poświęconego pojedynczemu awatarowi do kompletnego środowiska obejmującego dokumentację produkcyjną, walidatory, integracje z narzędziami DCC oraz aplikację desktopową prowadzącą użytkownika przez cały pipeline. Dotychczasowa nazwa `avatar-3d-self` opisuje historyczny cel repozytorium, ale nie oddaje aktualnej roli produktu.

## Decyzja

Kanoniczna nazwa produktu to **Avatar Studio**.

Stosujemy następujące identyfikatory:

- produkt i UI: `Avatar Studio`;
- moduł/import Python: `avatar_studio`;
- dystrybucja Python i komenda CLI: `avatar-studio`;
- executable: `AvatarStudio.exe` na Windows i `AvatarStudio` na Linux;
- stan lokalny projektu: `.avatar-studio/`.

Historyczny adres repozytorium GitHub może pozostać niezmieniony do czasu wykonania operacji administracyjnej zmiany nazwy repozytorium.

## Konsekwencje

Nowy kod, dokumentacja, artefakty aplikacji i przyszłe pakiety używają nazwy Avatar Studio. Stare identyfikatory pozostają wyłącznie tam, gdzie są częścią historycznego adresu URL lub wymagają osobnej migracji zewnętrznej.
