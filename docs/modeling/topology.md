# Topologia produkcyjna

Topologia ma wspierać deformację, blend shapes, skinning i eksport runtime.

## Wymagania

- quady w obszarach deformacji, trójkąty tylko tam, gdzie są kontrolowane;
- brak non-manifold geometry i niezamierzonych duplikatów;
- równomierna gęstość dopasowana do funkcji;
- dodatkowe pętle przy stawach i fałdach aktywnych;
- symetria może być użyta podczas budowy, ale finalny kształt nie powinien sztucznie usuwać naturalnej asymetrii.

## Edge flow ciała

Największej kontroli wymagają barki, pachy, łokcie, nadgarstki, pachwiny, pośladki, kolana i kostki. Pętle powinny pozwalać na kompresję po stronie zgięcia i rozciąganie po stronie przeciwnej bez gwałtownej utraty objętości.

## Topology freeze

Po zatwierdzeniu retopologii indeksy wierzchołków i podstawowa struktura siatki stają się kontraktem dla UV, blend shapes, skinningu i części narzędzi. Zmiana po tym punkcie wymaga jawnej migracji zależnych artefaktów.