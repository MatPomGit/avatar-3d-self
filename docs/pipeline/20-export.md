# 20. Eksport do środowiska docelowego

Eksport jest kontrolowanym przekształceniem zatwierdzonej wersji wzorcowej do artefaktu pochodnego przeznaczonego dla konkretnego środowiska docelowego. Nie jest końcem procesu. Kończy się dopiero po poprawnym imporcie i walidacji.

**Dane wejściowe:** zatwierdzona wersja wzorcowa sceny, profil eksportu, docelowy silnik i jego wersja.  
**Artefakt pochodny:** FBX, GLB, glTF, USD lub inny zatwierdzony format wraz z raportem konwersji.

## Profil eksportu

Profil eksportu powinien jawnie zawierać:

- format i wersję formatu;
- jednostkę długości;
- oś pionową;
- kierunek „przód”;
- regułę transformacji osi;
- sposób eksportu szkieletu;
- sposób eksportu celów morfowania;
- listę animacji;
- konwencję map normalnych;
- przestrzenie barw tekstur;
- pakowanie kanałów;
- poziomy szczegółowości;
- reguły włosów;
- reguły materiałów przezroczystych.

## Kontrola przed eksportem

Przed każdym eksportem sprawdź:

1. brak niezastosowanych przypadkowych transformacji;
2. prawidłową skalę;
3. poprawną pozę spoczynkową;
4. zgodność nazw kości;
5. zgodność nazw kształtów deformacyjnych;
6. poprawne ścieżki tekstur;
7. brak tymczasowych obiektów roboczych w zestawie eksportowym;
8. wersję sceny źródłowej.

## Windows

1. Zapisz nową wersję sceny wzorcowej przed eksportem.
2. Wybierz przypięty profil środowiska docelowego.
3. Eksportuj wyłącznie jawnie oznaczone obiekty.
4. Zapisz wersję programu DCC i eksportera.
5. Oblicz SHA-256 pliku wynikowego.
6. Zaimportuj plik do czystej sceny walidacyjnej środowiska docelowego.
7. Uruchom procedurę z [walidacji importu](../runtime/import-validation.md).

## Linux

1. Użyj tej samej wersji sceny i tego samego profilu eksportu.
2. Jeżeli eksport jest wykonywany wsadowo, zapisz pełne polecenie i wersję programu.
3. Zapisz raport utraconych lub zastąpionych funkcji.
4. Oblicz SHA-256 pliku wynikowego.
5. Wykonaj import do czystej sceny walidacyjnej.
6. Uruchom te same testy jak na Windows.

## Konwersje pośrednie

Każda dodatkowa konwersja, np. FBX -> GLB, zwiększa ryzyko utraty informacji. Dlatego zapisujemy cały łańcuch:

```text
master.blend
  -> avatar_unreal.fbx
  -> import Unreal
```

albo:

```text
master.blend
  -> avatar_interchange.fbx
  -> converter
  -> avatar_web.glb
  -> import Web
```

Jeżeli możliwy jest eksport bezpośredni bez utraty potrzebnych funkcji, preferujemy krótszy łańcuch.

## Raport eksportu

Raport zawiera co najmniej:

- identyfikator wersji źródłowej;
- profil eksportu;
- datę;
- wersje narzędzi;
- format wynikowy;
- sumę kontrolną;
- liczbę siatek;
- liczbę kości;
- liczbę kształtów deformacyjnych;
- listę animacji;
- listę ostrzeżeń;
- wynik importu testowego.

## Kryterium ukończenia

Etap eksportu jest zaliczony tylko wtedy, gdy import testowy potwierdza skalę, szkielet, kształty deformacyjne, materiały, animacje i wymagane poziomy szczegółowości. Sam komunikat „export successful” nie jest kryterium jakości.