# 19. Integracja Piper

**Input:** tekst, zatwierdzony model Piper i pipeline alignmentu.  
**Editable output:** konfiguracja głosu i mappingu.  
**Derived output:** WAV + phoneme timing + animation curves.

```text
text → Piper → audio.wav → phoneme alignment → timestamps
     → phoneme-to-viseme mapping → coarticulation → facial curves
```

## Windows

1. Uruchom Piper z lokalnym modelem i jawnie ustawionym sample rate.
2. Zapisz WAV bez ponownej kompresji stratnej.
3. Uruchom aligner i zapisz timestampy w JSON.
4. Wygeneruj viseme curves.
5. Zachowaj wersję modelu głosu w raporcie.

## Linux

1. Uruchom lokalny Piper z tą samą konfiguracją głosu.
2. Wygeneruj WAV PCM.
3. Uruchom alignment fonemów.
4. Wygeneruj identyczny format JSON timingów i krzywych.
5. Zweryfikuj zgodność czasu audio i animacji.

## DoD

Ten sam tekst daje audytowalny łańcuch artefaktów: tekst, audio, fonemy, visemy i wynikową animację. Brak kroku opartego wyłącznie na amplitudzie audio.
