# 20. Eksport

**Input:** zatwierdzona scena master.  
**Derived output:** FBX/GLB/USD według celu + conversion report.

## Windows

1. Zapisz master przed eksportem.
2. Ustal target format i konkretną wersję silnika.
3. Eksportuj tylko wymagane obiekty, skeleton, morph targets i animacje.
4. Zapisz units, axis conversion, texture paths i wersję eksportera.
5. Uruchom `model_format_converter.py` tylko gdy konwersja jest świadomie wymagana.

## Linux

1. Zachowaj identyczny master i profil eksportu.
2. Eksportuj przez Blender GUI lub jawnie zapisaną komendę CLI.
3. Zapisz raport potencjalnej utraty materiałów, morphs i animacji.
4. Oblicz hash pliku wynikowego.
5. Nie zastępuj mastera plikiem interchange.

## DoD

Import test w target environment potwierdza skalę, skeleton, morph targets, materiały i animacje. Sam sukces eksportera nie oznacza zaliczenia.
