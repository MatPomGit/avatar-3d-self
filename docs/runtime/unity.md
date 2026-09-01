# Unity

Unity jest drugim docelowym środowiskiem interoperacyjności. Nie zakładamy jednak, że parametry materiałów, twarzy i animacji można przenieść 1:1 z Unreal lub Blendera.

Profil Unity zawsze wskazuje dokładną wersję edytora oraz używany potok renderowania, np. HDRP albo URP.

## Renderowanie deformowalnej siatki

Komponent Skinned Mesh Renderer odpowiada za renderowanie siatki deformowanej przez kości i kształty deformacyjne. To w nim kończy się część danych szkieletu i twarzy po imporcie.

Po imporcie sprawdzamy:

- zgodność skali;
- kości i pozę wiązania;
- wagi wpływu kości;
- liczbę kształtów deformacyjnych;
- materiały;
- granice obiektu używane do odrzucania renderowania.

## Wagi kształtów deformacyjnych

W logice Avatar Studio kanały twarzy używają znormalizowanego zakresu 0-1. Interfejsy Unity dla kształtów deformacyjnych mogą operować skalą, w której 100 oznacza pełny wpływ.

Adapter powinien więc wykonywać jawne przeliczenie:

`unity_weight = avatar_weight * 100`

Przykładowo:

- `0.0` -> `0`;
- `0.25` -> `25`;
- `0.5` -> `50`;
- `1.0` -> `100`.

Nie zapisujemy tej różnicy w danych źródłowych. Jest to odpowiedzialność adaptera Unity.

## HDRP i URP

HDRP i URP nie są tylko ustawieniami jakości. Są różnymi potokami renderowania i mogą wymagać innych materiałów.

Dla fotorealistycznego profilu desktopowego HDRP jest naturalnym kandydatem do testów skóry, półprzezroczystości i oświetlenia wysokiej jakości. URP może być korzystniejszy na słabszym sprzęcie lub urządzeniach mobilnych.

Decyzja jest podejmowana na podstawie testu, nie na podstawie nazwy potoku.

## Skóra

Profil materiału skóry musi jawnie definiować:

- barwę bazową;
- chropowatość lub odpowiadający jej parametr silnika;
- mapy normalnych;
- rozpraszanie podpowierzchniowe, jeśli wybrany potok je obsługuje w wymaganej jakości;
- mikrodetal;
- sposób obsługi zmarszczek dynamicznych.

## Oczy i okulary

Weryfikujemy oddzielnie powierzchnie przezroczyste. Typowe problemy to:

- niewłaściwa kolejność renderowania;
- zbyt silne odbicia;
- brak głębi tęczówki;
- problemy z przezroczystością soczewek okularów;
- znikanie menisku łzowego w dalszym planie.

## Animacja

Klipy testowe są takie same jak dla Unreal. Nie tworzymy łatwiejszego zestawu testów tylko dlatego, że implementacja silnika jest inna.

## Windows

1. Przypnij wersję Unity i potok renderowania.
2. Zaimportuj identyczny artefakt pochodny jak w innych profilach.
3. Zweryfikuj siatkę, szkielet i kształty deformacyjne.
4. Odtwórz materiały.
5. Podłącz profil wizemów i animacji twarzy.
6. Uruchom klipy akceptacyjne.
7. Wykonaj profilowanie CPU, GPU i pamięci.

## Linux

1. Użyj tej samej wersji Unity i potoku renderowania.
2. Zaimportuj ten sam pakiet.
3. Porównaj deformację i materiały.
4. Zweryfikuj różnice backendu renderera.
5. Uruchom te same testy wydajnościowe.
6. Zapisz oddzielny raport.

## Kryterium zaliczenia

Profil Unity jest zaliczony, gdy postać zachowuje podobieństwo i pełną podstawową funkcjonalność animacyjną, a adapter nie wymaga ręcznego poprawiania każdego kolejnego eksportu.