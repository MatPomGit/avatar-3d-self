# Mapa dokumentacji

Ten dokument określa aktualny poziom pokrycia dokumentacji Avatar Studio. Po audycie rozróżniamy **kompletność zakresu** od **kompletności dydaktycznej**. Projekt obejmuje prawie wszystkie wymagane obszary tematyczne, ale nie każdy rozdział prowadzi jeszcze użytkownika wystarczająco szczegółowo przez wykonanie zadania.

Szczegółowe braki implementacyjne i dokumentacyjne opisuje [audyt gotowości przed dalszym rozwojem](pre-development-audit.md).

## Zakres pokrycia

| Obszar | Pokrycie zakresu | Kompletność dydaktyczna | Główne rozdziały |
| --- | --- | --- | --- |
| Cele, architektura i konwencje | kompletne | wysokie | `project/` |
| 21-etapowy pipeline produkcyjny | kompletne | częściowe | `pipeline/` |
| Pozyskiwanie referencji | kompletne | wysokie | `capture/` |
| Anatomia, modelowanie i topologia | kompletne | częściowe | `modeling/` |
| UV, PBR, skóra, oczy, włosy, ubrania i okulary | kompletne | dobre, nierówne | `materials/` |
| Szkielet, ciało, dłonie, twarz, ARKit/FACS i skinning | kompletne | dobre, nierówne | `rigging/` |
| Ruch ciała, mimika, spojrzenie, mruganie i bezczynność | kompletne | częściowe | `animation/` |
| Piper, fonemy, wizemy, koartykulacja i synchronizacja mowy | kompletne | dobre | `speech/` |
| Unreal Engine, Unity, Web, LOD i wydajność | kompletne | dobre | `runtime/` |
| Podobieństwo, geometria, deformacja, twarz i efekt doliny niesamowitości | kompletne | dobre | `validation/` |
| Blender, COLMAP, FFmpeg, Piper i konwersja formatów | kompletne | dobre | `tools/` |
| Aplikacja desktopowa Avatar Studio | architektura kompletna, funkcje częściowe | wymaga aktualizacji względem GUI | `desktop/` |
| Instalacja Windows i Linux | bazowe | częściowe | `setup/` |
| Decyzje architektoniczne | kompletne dla obecnego stanu | wysokie | `adr/` |

## Co oznacza kompletność dokumentacji

Dokumentacja bazowa jest wystarczająca zakresowo, jeśli odpowiada na pytania:

1. Czym jest dany etap lub parametr?
2. Dlaczego jest potrzebny w Avatar Studio?
3. Jakie są typowe wartości, zakresy lub warianty?
4. Jak rozpoznać wynik błędny lub niewystarczający?
5. Jakie artefakty i testy kończą etap?

Dokumentacja dydaktyczna etapu jest kompletna dopiero wtedy, gdy dodatkowo zawiera:

1. przygotowanie wejść i środowiska;
2. dokładną procedurę krok po kroku;
3. wskazanie programu, ekranu lub kontrolki GUI używanej w każdym kroku;
4. opis parametrów wraz z bezpiecznymi wartościami początkowymi;
5. kontrolę pośrednią wyniku;
6. typowe błędy i ich rozpoznawanie;
7. procedurę naprawczą;
8. oczekiwany artefakt końcowy i kryteria Definition of Done.

Wartości liczbowe, które mają znaczenie dla automatycznej walidacji, powinny być przenoszone do `config/technical_baselines.yaml`, aby dokumentacja i kod nie utrzymywały niezależnych kopii tych samych danych.

## Priorytet rozbudowy dydaktycznej

Najpilniejszego rozwinięcia wymagają rozdziały pipeline'u dotyczące:

- fotogrametrii i wyboru parametrów rekonstrukcji;
- dense reconstruction i meshing;
- cleanupu high-poly;
- retopologii;
- UV;
- rigu ciała i twarzy;
- skinningu;
- eksportu;
- walidacji runtime.

Dokumenty szczegółowe w `capture/`, `materials/`, `rigging/`, `speech/` i `runtime/` mogą pełnić rolę rozwinięć, ale rozdział pipeline'u powinien zawsze wskazywać dokładnie, kiedy i po co użytkownik ma do nich przejść.

## Dokumentacja a implementacja

Warstwa dokumentacyjna może opisywać funkcje planowane, ale status implementacji musi być jawny. Funkcje aplikacji desktopowej należy oznaczać jako `implemented`, `partial` albo `planned`, jeśli opis może sugerować użytkownikowi, że dana operacja jest już dostępna w GUI.

Roadmapa produktu obejmuje między innymi integrację operacji narzędzi z interfejsem, podgląd wyników, automatyczne raporty, pakowanie aplikacji oraz demonstrator czasu rzeczywistego.

Jeżeli podczas implementacji pojawi się nowy podsystem, który zmienia kontrakt pipeline'u, dokumentacja musi zostać rozszerzona przed uznaniem danego podsystemu za gotowy.

## Pokrycie MkDocs

Każdy plik Markdown znajdujący się pod `docs/`, poza plikami jawnie wyłączonymi z publikacji, musi znajdować się w `nav` w `mkdocs.yml`. Kontrola jest wykonywana automatycznie w CI przez `scripts/check_mkdocs_coverage.py`.

W praktyce oznacza to, że utworzenie nowego dokumentu bez dodania go do nawigacji powoduje błąd walidacji. Dzięki temu nie powstają dokumenty dostępne jedynie przez bezpośredni URL i niewidoczne w strukturze GitHub Pages.

## Kryterium zamknięcia warstwy dokumentacyjnej

Warstwę dokumentacyjną projektu można uznać za zamkniętą na poziomie dydaktycznym, gdy jednocześnie:

- wszystkie obszary z tabeli mają jawny status;
- wszystkie etapy pipeline'u spełniają kryteria instrukcji krok po kroku opisane powyżej;
- instrukcja GUI odpowiada rzeczywistej wersji programu;
- funkcje planowane są wyraźnie odróżnione od działających;
- `mkdocs build --strict` kończy się powodzeniem;
- kontrola pokrycia MkDocs nie wykrywa osieroconych plików Markdown;
- kontrola terminologii nie wykrywa zabronionych form;
- aktywne linki lokalne nie prowadzą do nieistniejących dokumentów;
- GitHub Pages publikuje wynik z bieżącej gałęzi `main`.
