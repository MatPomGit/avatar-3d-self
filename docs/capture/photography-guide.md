# Fotografia do rekonstrukcji i referencji

Celem capture jest uzyskanie danych o geometrii i wyglądzie, a nie estetycznego portretu. Beauty filters, portrait blur, zmienna ekspozycja i agresywne HDR obniżają wartość pomiarową.

## Stanowisko

Użyj rozproszonego, możliwie stałego światła. Tło powinno być matowe i nieruchome. Dla geometrii unikaj ostrych cieni i połysków. Do osobnej sesji materiałowej można użyć światła kierunkowego do oceny roughness i mikrogeometrii, ale nie mieszaj jej ze zdjęciami rekonstrukcyjnymi.

## Kamera

Preferuj główny aparat 1× telefonu lub obiektyw o małym zniekształceniu perspektywicznym. Zachowaj tę samą ogniskową, rozdzielczość, orientację i parametry w obrębie serii. RAW jest wartościowy jako archiwum, ale pipeline fotogrametryczny może pracować na spójnie wywołanych kopiach.

## Operator i samodzielny capture

**Operator:** osoba pozostaje nieruchoma, kamera porusza się po pierścieniach. To wariant preferowany, bo obiekt nie zmienia kształtu między zdjęciami.

**Samodzielnie:** kamera stoi na statywie, a osoba obraca całe ciało o 10–15° między ujęciami. Jest to kompromis: ubrania, włosy i tkanki mogą zmieniać położenie, dlatego serie wykonuj wolno i bez zmiany pozy kończyn. Nie mieszaj obu metod w jednej rekonstrukcji bez testu.

## Twarz

Wykonaj trzy pierścienie: wysokość oczu, około 20 cm wyżej i około 20 cm niżej. Zachowaj 70–80% pokrycia sąsiednich kadrów. Szczególnie dopilnuj uszu, linii włosów, nosa, skrzydełek nosa, żuchwy i spodu brody.

## Sylwetka

Użyj A-pose z ramionami odsuniętymi od tułowia 30–45°, rozstawionymi palcami i równoległymi stopami. Wykonaj pełne pierścienie na kilku wysokościach. Nie zasłaniaj pach, wewnętrznych stron kończyn i dłoni.

## Dłonie

Fotografuj każdą dłoń oddzielnie: grzbiet, wnętrze, krawędź promieniową i łokciową oraz widoki palców. Do modelowania paznokci i skóry wykonaj dodatkową serię macro/reference, niezależną od rekonstrukcji całej sylwetki.

## Okulary

Refleksy i przezroczystość są trudne dla fotogrametrii. Geometrię okularów odtwarzaj przede wszystkim z osobnych zdjęć i pomiarów. Jeśli okulary są kluczowe dla podobieństwa, wykonaj referencje z nimi, ale rozważ dodatkową serię twarzy bez okularów do geometrii skóry wokół oczu.

## Windows: organizacja materiału

```powershell
mkdir D:\Avatar3D\projects\self-avatar\capture\face
mkdir D:\Avatar3D\projects\self-avatar\capture\body
mkdir D:\Avatar3D\projects\self-avatar\capture\hands
mkdir D:\Avatar3D\projects\self-avatar\capture\expressions
mkdir D:\Avatar3D\projects\self-avatar\capture\rejected
```

Zachowaj oryginały jako read-only backup i pracuj na kopii.

## Linux: organizacja materiału

```bash
mkdir -p ~/Avatar3D/projects/self-avatar/capture/{face,body,hands,expressions,rejected}
```

Zachowaj niezmienione oryginały i pracuj na kopii.

## Odrzucanie klatek

Odrzuć: motion blur, mrugnięcie w neutralnej serii, zmianę zoomu, zmianę pozy, częściowe zasłonięcie obiektu, clipped highlights na dużej części skóry, silny rolling-shutter deformation i zdjęcia przetworzone innym profilem niż reszta serii.
