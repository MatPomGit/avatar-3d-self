# Pipeline produkcyjny

Poniższe etapy zachowują edytowalność awatara. Etap jest ukończony dopiero po przejściu wskazanej kontroli jakości.

## 1. Referencje

Zbierz widoki twarzy i sylwetki, ubrania oraz okulary. Zapisz warunki zdjęć, skalę i zgodę na użycie materiałów.

**Kontrola:** komplet widoków, neutralna mimika, widoczne cechy charakterystyczne.

## 2. Rekonstrukcja

Wykonaj lokalną rekonstrukcję i zachowaj oryginalne zdjęcia, wynik rekonstrukcji oraz oczyszczoną siatkę jako osobne artefakty.

**Kontrola:** poprawna skala i orientacja, brak istotnych ubytków.

## 3. Model, UV i materiały

Wykonaj topologię dla deformacji, UV oraz oddzielne komponenty ciała, oczu, zębów, włosów, brody, ubrań i okularów. Przygotuj materiały PBR.

**Kontrola:** brak rozciągania UV, szwów i błędów materiałowych.

## 4. Rig i animacja

Przygotuj rig ciała, dłoni, oczu i twarzy oraz mapowanie ARKit/FACS. Sprawdź mrugnięcie, żuchwę, uśmiech, palce, barki i kolana.

**Kontrola:** naturalne deformacje w zestawie testowych póz.

## 5. Mowa

Docelowy łańcuch to: tekst, Piper, czas fonemów lub visemów, animacja twarzy, odtworzenie w silniku. Łącz visemy z ruchem szczęki, spojrzeniem, mruganiem, głową i emocją.

**Kontrola:** zgodność głosek, brak dryfu audio oraz martwego spojrzenia.

## 6. Eksport i środowisko docelowe

Eksportuj model z raportem konwersji. Waliduj geometrię, materiały, rig, skinning, shape keys i animacje po imporcie do wybranego silnika.

**Kontrola:** działająca scena z bezczynnością, mową, emocją i gestem w założonym budżecie wydajności.

GitHub Actions nie zastępują tych kontroli. Obsługują tylko lekką walidację i stronę statyczną.
