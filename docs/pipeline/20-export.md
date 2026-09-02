# 20. Eksport

**Input:** zatwierdzony model, materiały, rig, animacje i dane mowy.  
**Editable output:** profil eksportowy i scena źródłowa.  
**Derived output:** paczka runtime, raport konwersji i walidacja importu.

## Cel etapu

Eksport nie jest zwykłym zapisaniem FBX lub glTF. Jest kontrolowanym przejściem z kanonicznej sceny edytowalnej do konkretnego środowiska runtime. Każdy profil eksportowy musi jawnie określać osie, jednostki, skalę, skeleton, morph targets, tekstury, animacje i ograniczenia formatu.

## Przygotowanie

1. Zablokuj wersję źródłowej sceny `.blend`.
2. Wybierz środowisko docelowe: Unreal Engine, Unity lub Web.
3. Odczytaj odpowiednią instrukcję w sekcji `runtime/`.
4. Ustal format wymiany i jego ograniczenia.
5. Zapisz profil eksportu zamiast zmieniać ustawienia ręcznie przy każdej wersji.

## Wspólne kontrole przed eksportem

Sprawdź:

- jednostki i skalę;
- globalne osie i handedness;
- rest pose;
- nazwy kości;
- brak control bones w eksporcie, jeśli nie są potrzebne;
- liczbę influences per vertex;
- obecność wymaganych morph targets;
- zakres animacji i FPS;
- ścieżki tekstur;
- przestrzenie barw map PBR;
- zgodność groom/hair z silnikiem docelowym.

## FBX

FBX jest praktyczny dla wielu pipeline'ów Unreal/Unity, ale jego zachowanie zależy od eksportera i importera. Przed eksportem:

1. zaznacz wyłącznie obiekty przeznaczone do runtime;
2. wyłącz eksport niepotrzebnych kamer i świateł;
3. upewnij się, że armature nie dostaje dodatkowego sztucznego root bone przez ustawienia eksportera;
4. sprawdź bake animacji i zakres klatek;
5. potwierdź eksport blend shapes/morph targets;
6. zapisz dokładną wersję Blendera i parametry eksportera w raporcie.

## glTF/GLB

glTF jest preferowany dla interoperacyjności i Web, ale nie wszystkie funkcje DCC mają bezpośredni odpowiednik. Sprawdź szczególnie:

- obsługę morph targets;
- materiały PBR;
- ograniczenia skeletonu;
- animacje;
- brak natywnego odpowiednika niektórych systemów groom i constraintów.

Nie traktuj poprawnego otwarcia GLB w jednym viewerze jako pełnej walidacji runtime.

## Tekstury

Dla każdej mapy zapisz:

- nazwę materiału;
- rolę mapy;
- rozdzielczość;
- bit depth;
- color space;
- kanały pakowane;
- format pliku.

Base Color zwykle korzysta z przestrzeni sRGB, a mapy danych takie jak roughness, metallic, normal czy AO powinny być traktowane jako dane liniowe zgodnie z profilem silnika.

## Skeleton i animacje

Przed eksportem wykonaj test:

1. neutral pose;
2. pełny zakres ruchu kończyn;
3. animację twarzy;
4. kilka morph targets ARKit;
5. klip mowy;
6. animację zawierającą jednocześnie ciało i twarz.

Po eksporcie sprawdź, czy liczba kości i morph targets nie zmieniła się nieoczekiwanie.

## Włosy i ruch wtórny

Hair groom, cloth i secondary motion często wymagają osobnego workflow specyficznego dla silnika. Jeżeli format wymiany nie przenosi symulacji, eksportuj geometrię/guide data i odtwórz solver w runtime zgodnie z dokumentacją targetu.

## Automatyczne narzędzia repozytorium

Projekt zawiera skrypty pomocnicze m.in. do:

- eksportu FBX;
- konwersji formatów;
- walidacji FBX;
- optymalizacji materiałów i tekstur;
- generowania LOD;
- eksportu do Unreal.

Skrypty należy traktować jako część odtwarzalnego pipeline'u. Ich parametry powinny trafić do raportu konwersji.

## Raport eksportu

Raport powinien zawierać:

1. SHA-256 sceny źródłowej;
2. wersję narzędzia eksportującego;
3. format i wersję eksportera;
4. jednostki i osie;
5. listę obiektów;
6. liczbę kości;
7. liczbę morph targets;
8. liczbę animacji;
9. listę tekstur;
10. hash wynikowego pliku;
11. ostrzeżenia i świadome wyjątki.

## Import kontrolny

Nie zaliczaj etapu na podstawie samego utworzenia pliku. Zaimportuj wynik do pustego projektu docelowego i sprawdź:

- skalę postaci;
- orientację;
- bind pose;
- ruch kończyn;
- twarz i blink;
- materiały;
- normal maps;
- przezroczystość włosów i soczewek;
- klip mowy.

## Typowe błędy

### Postać ma złą skalę

Porównaj jednostki sceny, global scale eksportera i ustawienia importera. Nie koryguj problemu przypadkową skalą obiektu w runtime bez zapisania przyczyny.

### Kości są obrócone po imporcie

Sprawdź osie lokalne, rest pose oraz axis conversion. Problem nie powinien być naprawiany edycją animacji klatka po klatce.

### Znikają blend shapes

Sprawdź opcję eksportu morph targets i czy topology/vertex order nie zostały zmienione po ich utworzeniu.

### Materiały wyglądają inaczej

Sprawdź color space, kanały roughness/metallic/AO, normal map convention oraz shader docelowego silnika.

## Validation

Eksport jest poprawny, gdy:

- wynik można odtworzyć z profilu i sceny źródłowej;
- skala i orientacja są zgodne;
- skeleton i morph targets są kompletne;
- animacje przechodzą import kontrolny;
- materiały są mapowane zgodnie z profilem targetu;
- hash i raport zostały zapisane.

## DoD

Powstaje wersjonowana paczka runtime wraz z raportem konwersji. Sam plik FBX/GLB bez raportu i testu importu nie spełnia Definition of Done.
