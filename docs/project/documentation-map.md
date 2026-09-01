# Mapa dokumentacji

Ten dokument określa, które obszary projektu Avatar Studio mają już kompletną dokumentację bazową. „Kompletna” oznacza, że opisano zakres, wymagania, wartości bazowe, kryteria odbioru oraz powiązania z pozostałymi etapami. Nie oznacza to zakończenia implementacji produktu ani zakazu dalszego rozszerzania dokumentacji.

## Zakres pokrycia

| Obszar | Dokumentacja bazowa | Główne rozdziały |
| --- | --- | --- |
| Cele, architektura i konwencje | kompletna | `project/` |
| 21-etapowy pipeline produkcyjny | kompletna | `pipeline/` |
| Pozyskiwanie referencji | kompletna | `capture/` |
| Anatomia, modelowanie i topologia | kompletna | `modeling/` |
| UV, PBR, skóra, oczy, włosy, ubrania i okulary | kompletna | `materials/` |
| Szkielet, ciało, dłonie, twarz, ARKit/FACS i skinning | kompletna | `rigging/` |
| Ruch ciała, mimika, spojrzenie, mruganie i bezczynność | kompletna | `animation/` |
| Piper, fonemy, wizemy, koartykulacja i synchronizacja mowy | kompletna | `speech/` |
| Unreal Engine, Unity, Web, LOD i wydajność | kompletna | `runtime/` |
| Podobieństwo, geometria, deformacja, twarz i efekt doliny niesamowitości | kompletna | `validation/` |
| Blender, COLMAP, FFmpeg, Piper i konwersja formatów | kompletna | `tools/` |
| Aplikacja desktopowa Avatar Studio | kompletna baza architektoniczna i operacyjna | `desktop/` |
| Instalacja Windows i Linux | kompletna baza | `setup/` |
| Decyzje architektoniczne | kompletna dla obecnego stanu projektu | `adr/` |

## Co oznacza kompletność dokumentacji

Dokumentacja bazowa jest uznawana za kompletną, jeśli dla każdego kluczowego elementu pipeline'u istnieje odpowiedź na pięć pytań:

1. Czym jest dany etap lub parametr?
2. Dlaczego jest potrzebny w Avatar Studio?
3. Jakie są typowe wartości, zakresy lub warianty?
4. Jak rozpoznać wynik błędny lub niewystarczający?
5. Jakie artefakty i testy kończą etap?

Wartości liczbowe, które mają znaczenie dla automatycznej walidacji, powinny być przenoszone do `config/technical_baselines.yaml`, aby dokumentacja i kod nie utrzymywały niezależnych kopii tych samych danych.

## Dokumentacja a implementacja

Warstwa dokumentacyjna może być kompletna mimo tego, że implementacja programu nadal jest rozwijana. Roadmapa produktu obejmuje między innymi integrację operacji narzędzi z interfejsem, podgląd wyników, automatyczne raporty, pakowanie aplikacji oraz demonstrator czasu rzeczywistego.

Jeżeli podczas implementacji pojawi się nowy podsystem, który zmienia kontrakt pipeline'u, dokumentacja musi zostać rozszerzona przed uznaniem danego podsystemu za gotowy.

## Pokrycie MkDocs

Każdy plik Markdown znajdujący się pod `docs/`, poza plikami jawnie wyłączonymi z publikacji, musi znajdować się w `nav` w `mkdocs.yml`. Kontrola jest wykonywana automatycznie w CI przez `scripts/check_mkdocs_coverage.py`.

W praktyce oznacza to, że utworzenie nowego dokumentu bez dodania go do nawigacji powoduje błąd walidacji. Dzięki temu nie powstają dokumenty dostępne jedynie przez bezpośredni URL i niewidoczne w strukturze GitHub Pages.

## Kryterium zamknięcia warstwy dokumentacyjnej

Warstwę dokumentacyjną projektu można uznać za zamkniętą na poziomie bazowym, gdy jednocześnie:

- wszystkie obszary z tabeli mają status „kompletna” lub jawnie opisany status częściowy;
- `mkdocs build --strict` kończy się powodzeniem;
- kontrola pokrycia MkDocs nie wykrywa osieroconych plików Markdown;
- kontrola terminologii nie wykrywa zabronionych form;
- aktywne linki lokalne nie prowadzą do nieistniejących dokumentów;
- GitHub Pages publikuje wynik z bieżącej gałęzi `main`.
