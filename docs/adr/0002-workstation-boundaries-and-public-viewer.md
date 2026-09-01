# ADR-0002: Środowiska robocze i publiczny viewer

**Status:** zaakceptowana, 2026-09-01

## Kontekst

COLMAP, Blender, MetaHuman, Unreal Engine i osobisty Piper są środowiskami lokalnymi. Materiały referencyjne oraz głos są wrażliwe.

## Decyzja

GitHub Actions wykonują tylko deterministyczne kontrole i wdrażają stronę statyczną. Specjalistyczne przetwarzanie pozostaje ręczne, aż do przygotowania powtarzalnego runnera i zatwierdzonych danych testowych.

## Konsekwencje

Prywatne zdjęcia, skany, nagrania i dane dostępu nie trafiają do publicznego repozytorium ani viewera.
