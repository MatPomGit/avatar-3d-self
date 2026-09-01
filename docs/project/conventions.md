# Konwencje

## Nazewnictwo

- Python: `snake_case`, klasy `PascalCase`, stałe `UPPER_CASE`.
- Markdown i katalogi zasobów: `kebab-case`.
- Kości, kształty deformacyjne (blend shapes) i nazwy wymagane przez zewnętrzne standardy zachowują ich kanoniczną pisownię.
- Pliki kolejnych wersji artefaktów używają jawnego numeru `vNNN`.

## Terminologia dokumentacji

Kanonicznym źródłem polskich terminów jest [słownik terminologiczny](terminology.md).

W tekście dydaktycznym i opisowym stosujemy formę **polska nazwa (angielski termin)**, np. **przestrzeń barw (color space)**, **głębia bitowa (bit depth)**, **gęstość tekseli (texel density)** oraz **współczynnik załamania światła (Index of Refraction, IOR)**.

Nie tworzymy prostych kalek językowych, jeżeli istnieje poprawny polski termin. Angielski identyfikator pozostaje bez tłumaczenia tylko wtedy, gdy jest częścią kontraktu technicznego, np. `roughness`, `BaseColor`, `jawOpen`, nazwa pola JSON, nazwa funkcji, ścieżka pliku albo wymagany identyfikator standardu.

Nowy powtarzalny termin techniczny należy najpierw dopisać do słownika, a dopiero potem stosować w kolejnych dokumentach.

### Dydaktyczne wprowadzenie nowego pojęcia

Przy pierwszym omawianiu nowego pojęcia w rozdziale nie zaczynamy od tabeli parametrów ani od skrótu. Najpierw wyjaśniamy czytelnikowi:

1. czym jest dane pojęcie;
2. do czego służy w projekcie Avatar Studio;
3. co w praktyce powoduje zwiększenie albo zmniejszenie jego wartości;
4. jaki jest typowy zakres wartości;
5. jakie wartości można uznać za niskie, typowe i wysokie;
6. w jakich sytuacjach wybiera się poszczególne wartości;
7. jakie objawy wskazują, że parametr jest ustawiony zbyt nisko albo zbyt wysoko.

Dla parametru liczbowego preferowany schemat dydaktyczny to:

> **Co to jest?** Krótkie wyjaśnienie znaczenia fizycznego lub technicznego.  
> **Co zmienia?** Opis wpływu zmiany wartości na wynik.  
> **Przykładowe wartości:** wartość niska, typowa i wysoka wraz z jednostką.  
> **Kiedy stosować?** Przykładowe sytuacje produkcyjne.  
> **Jak rozpoznać błąd?** Typowy artefakt przy wartości zbyt małej lub zbyt dużej.

Nie należy stosować tego jako sztywnego bloczka w każdym miejscu. Informacje mogą być zapisane płynnym tekstem, tabelą lub krótkim przykładem. Obowiązkowa jest treść dydaktyczna, a nie konkretny układ wizualny.

## Kod

Python 3.11, PEP 8 i PEP 257. Preferowane są małe moduły, jawne zależności i KISS. Adapter do zewnętrznego programu nie może mieszać logiki domenowej z analizowaniem interfejsu użytkownika.

## Dokumentacja procedur

Każda procedura zależna od systemu operacyjnego musi mieć osobne sekcje **Windows** i **Linux**. Nie używaj jednego bloku poleceń z komentarzem „na Windows zmień ścieżkę”.

Procedura techniczna powinna podawać kolejno: wymagania wstępne (prerequisites), dane wejściowe (input), kroki, oczekiwany wynik (expected output), walidację (validation) i procedurę odzyskiwania po błędzie (recovery). Nie zastępuj polecenia ogólnym stwierdzeniem typu „skonfiguruj poprawnie”.