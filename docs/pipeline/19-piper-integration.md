# 19. Integracja Piper

**Dane wejściowe (input):** tekst, zatwierdzony model Piper i profil syntezy.  
**Edytowalny wynik (editable output):** konfiguracja głosu, mapowanie fonemów i wizemów oraz parametry koartykulacji.  
**Wynik pochodny (derived output):** WAV, czasy fonemów i krzywe animacji.

```text
tekst → Piper → audio.wav → normalizacja fonemów → dopasowanie czasowe
      → fonem → wizem → koartykulacja → krzywe twarzy
```

## Dlaczego audio nie wystarcza

Amplituda sygnału mówi, kiedy dźwięk jest głośniejszy lub cichszy, ale nie mówi, czy mówca wypowiada `/m/`, `/f/`, `/a/` czy `/u/`. Dlatego sterowanie ustami wyłącznie amplitudą prowadzi do losowego otwierania i zamykania żuchwy.

## Windows

1. Uruchom lokalny Piper z zatwierdzonym modelem i profilem parametrów.
2. Zapisz WAV PCM bez stratnej kompresji.
3. Zapisz metadane modelu i parametrów syntezy.
4. Pobierz lub wyznacz czasy fonemów.
5. Znormalizuj symbole do [profilu języka polskiego](../speech/polish-phoneme-profile.md).
6. Zapisz wynik w [kanonicznym formacie dopasowania](../speech/alignment-format.md).
7. Wygeneruj wizemy i koartykulację.
8. Zweryfikuj wynik z audio i bez audio.

## Linux

Wykonaj te same kroki. Różnią się wyłącznie ścieżki środowiska i sposób uruchamiania procesu lub usługi Piper. Format WAV, JSON i parametry animacji pozostają identyczne.

## Walidacja

Dla krótkiego zdania testowego zapisujemy cały łańcuch:

- tekst;
- identyfikator i wersję modelu;
- parametry syntezy;
- skrót SHA-256 WAV;
- fonemy źródłowe;
- fonemy znormalizowane;
- wizemy;
- krzywe wynikowe.

Zmiana tekstu, modelu, `length_scale` albo pliku WAV unieważnia wszystkie późniejsze artefakty.

## Definition of Done

Etap jest zaliczony, gdy ten sam zestaw wejściowy daje audytowalny i odtwarzalny łańcuch danych, a synchronizacja nie opiera się wyłącznie na amplitudzie audio.
