# Piper TTS

Piper generuje audio głosu avatara. Audio nie jest jednak wystarczającym sygnałem sterującym dla ust.

## Kontrakt

Wejście: tekst i ustawienia głosu. Wyjście: WAV oraz metadane generacji. Następnie osobny aligner wyznacza czasy fonemów.

Model głosu, jego pliki konfiguracyjne i dane treningowe powinny być przechowywane oddzielnie od publicznej dokumentacji. Avatar Studio ma przechowywać jedynie ścieżki i jawne metadane, nie kopiować prywatnego modelu do repozytorium.

## Windows

Piper uruchamiaj jako lokalny proces z jawnie wskazaną ścieżką modelu i pliku wyjściowego.

## Linux

Stosuj ten sam kontrakt plikowy. Różni się jedynie ścieżka wykonywalna i sposób aktywacji środowiska.