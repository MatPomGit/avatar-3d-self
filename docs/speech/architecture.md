# Architektura mowy

```text
text
 ↓
Piper TTS
 ↓
audio PCM
 ↓
phoneme alignment
 ↓
phoneme timestamps
 ↓
phoneme → viseme mapping
 ↓
coarticulation model
 ↓
face + jaw curves
 ↓
layered facial animation
```

## Zasady

Lip-sync nie jest wyznaczany z samej amplitudy. Fonemy dają zdarzenia czasowe, a visemy są warstwą sterowania twarzą. Samogłoski zwykle mają dłuższe przejścia, a spółgłoski zwarte wymagają krótkich, czytelnych closures.

Koartykulacja obejmuje anticipatory blending przed fonemem oraz carry-over po nim. Parametry powinny być możliwe do kalibracji na indywidualnym modelu twarzy i języku.

## Windows

Piper, aligner i generator krzywych zapisują artefakty pośrednie w workspace. Każdy krok ma osobny log i wersję narzędzia.

## Linux

Format artefaktów musi być identyczny. Ścieżki absolutne nie mogą być zapisywane w przenośnych mappingach; aplikacja rozwiązuje je względem workspace.
