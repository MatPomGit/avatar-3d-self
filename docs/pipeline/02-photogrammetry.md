# 02. Fotogrametria

**Input:** zatwierdzone serie zdjęć.  
**Editable output:** projekt rekonstrukcji z parametrami kamery i dopasowaniem obrazów.  
**Derived output:** sparse point cloud, raport pokrycia.

## Windows

1. Utwórz osobny katalog roboczy dla serii twarzy i ciała.
2. Zaimportuj zdjęcia do COLMAP bez zmiany rozdzielczości.
3. Wykonaj feature extraction i matching dla zdjęć z jednej spójnej serii.
4. Uruchom sparse reconstruction.
5. Sprawdź liczbę zarejestrowanych zdjęć i rozmieszczenie kamer.
6. Usuń błędne zdjęcia dopiero po zapisaniu raportu przyczyny.

## Linux

1. Utwórz osobny katalog roboczy dla serii twarzy i ciała.
2. Zaimportuj oryginalne zdjęcia do COLMAP.
3. Wykonaj feature extraction i matching dla jednej serii.
4. Uruchom sparse reconstruction.
5. Sprawdź liczbę zarejestrowanych zdjęć i rozmieszczenie kamer.
6. Udokumentuj każde odrzucone zdjęcie.

## Validation

Wymagane jest stabilne pokrycie 360°, brak dużych luk wokół uszu, żuchwy, pach i dłoni oraz sensowna geometria trajektorii kamer. Nie kontynuuj dense reconstruction, jeżeli sparse model jest fragmentaryczny.

## DoD

Sparse model rejestruje zatwierdzoną większość zdjęć, nie ma dużych obszarów bez obserwacji, a parametry rekonstrukcji są zapisane.
