# ADR-0003: Kontrola twarzy i mowy

**Status:** zaakceptowana, 2026-09-01

## Kontekst

Sterowanie twarzą wyłącznie amplitudą audio daje nienaturalny efekt.

## Decyzja

System twarzy korzysta z mapowania zgodnego z ARKit, FACS albo jawnej transformacji między nimi. Mowa wykorzystuje czas fonemów lub visemów oraz warstwy ruchu szczęki, spojrzenia, mrugania, głowy i emocji.

## Konsekwencje

Każdy eksport zawiera lub wskazuje swoje mapowanie. Generator visemów wymaga walidacji na rzeczywistym głosie i w środowisku docelowym.
