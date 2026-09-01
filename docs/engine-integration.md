# Integracja z silnikami

Pierwsze środowisko docelowe nie zostało jeszcze wybrane. Ten dokument opisuje kontrolę importu, nie deklaruje gotowej integracji wielosilnikowej.

## Pakiet importowy

Każdy eksport zawiera:

- model i raport konwersji;
- jednostki, orientację i aplikację źródłową;
- tekstury PBR;
- mapowanie szkieletu, skinningu i morph targets;
- mapowanie animacji oraz visemów, jeśli występuje mowa;
- krótki klip walidacyjny i znane ograniczenia.

## Unreal Engine

Dla szkieletu i morph targets używaj FBX wyłącznie po sprawdzeniu importu w konkretnej wersji silnika. Zweryfikuj jednostki, materiały, LOD, kierunek oczu i krzywe animacji twarzy.

## Unity

Wybierz FBX lub GLB po kontroli importowanego rigu i nazw blendshape. Materiały odtwórz dla używanego URP albo HDRP.

## Viewer WWW

Viewer używa publicznego GLB/glTF. Nie zawiera zdjęć źródłowych, nagrań głosu, kluczy API ani niezatwierdzonych danych osobowych.

## Kontrola końcowa

W docelowym środowisku odtwórz klip z bezczynnością, mruganiem, spojrzeniem, mową, emocją i gestem. Zmierz czas klatki, pamięć, draw calls, liczbę trójkątów, materiały, tekstury i koszt animacji. Wynik workflow nie jest dowodem poprawności importu.
