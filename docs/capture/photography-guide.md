# Fotografia do rekonstrukcji i referencji

Celem capture jest uzyskanie danych o geometrii i wyglądzie, a nie estetycznego portretu. Beauty filters, portrait blur, zmienna ekspozycja i agresywne HDR obniżają wartość pomiarową.

## Stanowisko

Użyj rozproszonego, możliwie stałego światła. Tło powinno być matowe i nieruchome. Dla geometrii unikaj ostrych cieni i połysków. Do osobnej sesji materiałowej można użyć światła kierunkowego do oceny roughness i mikrogeometrii, ale nie mieszaj jej ze zdjęciami rekonstrukcyjnymi.

## Kamera

Preferuj główny aparat 1× telefonu lub obiektyw o małym zniekształceniu perspektywicznym. Zachowaj tę samą ogniskową, rozdzielczość, orientację i parametry w obrębie serii. RAW jest wartościowy jako archiwum, ale pipeline fotogrametryczny może pracować na spójnie wywołanych kopiach.

## Operator i samodzielny capture

**Operator:** osoba pozostaje nieruchoma, kamera porusza się po pierścieniach. To wariant najbardziej zgodny z klasyczną fotogrametrią statycznej sceny.

**Samodzielnie, obracająca się osoba:** kamera stoi na statywie, a osoba obraca całe ciało między ujęciami. Ten wariant jest oficjalnie wspierany, ponieważ jest praktycznie niezbędny przy samodzielnym fotografowaniu własnej sylwetki. Wymaga jednak segmentacji foreground, stałej pozy, kontrolowanych kroków kątowych oraz solve prowadzonego obiektocentrycznie, tak aby nieruchome tło nie sterowało rekonstrukcją.

Baseline dla sylwetki to krok 10° i 36 pozycji na pełne 360°. Każdy krok wykonuje się całym ciałem razem ze stopami, a nie przez skręcenie tułowia. Po zajęciu pozy należy odczekać około 2 s przed zdjęciem.

Szczegółowy workflow znajduje się w [przewodniku dla obracającej się osoby](rotating-subject-capture.md). Ogólne zasady self-capture opisuje [osobny dokument](self-capture.md).

## Twarz

Wykonaj trzy pierścienie: wysokość oczu, około 20 cm wyżej i około 20 cm niżej. Zachowaj 70–80% pokrycia sąsiednich kadrów. Szczególnie dopilnuj uszu, linii włosów, nosa, skrzydełek nosa, żuchwy i spodu brody.

## Sylwetka

Użyj A-pose z ramionami odsuniętymi od tułowia 30–45°, rozstawionymi palcami i równoległymi stopami. Wykonaj pełne pierścienie na kilku wysokościach albo, w wariancie samodzielnym, pełne obroty osoby dla kolejnych wysokości kamery. Nie zasłaniaj pach, wewnętrznych stron kończyn i dłoni.

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

Odrzuć: motion blur, mrugnięcie w neutralnej serii, zmianę zoomu, zmianę pozy kończyn, częściowe zasłonięcie obiektu, clipped highlights na dużej części skóry, silny rolling-shutter deformation i zdjęcia przetworzone innym profilem niż reszta serii.

Dla `rotating_subject` dodatkowo odrzuć klatki, w których miednica wyraźnie zeszła z osi obrotu, ręce zmieniły ułożenie, włosy nadal poruszają się po obrocie albo tło zostało błędnie uwzględnione w masce foreground.
