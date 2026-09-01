# Walidacja wiązania skóry z kośćmi

Wiązanie skóry z kośćmi (skinning) określa, jak mocno poszczególne kości wpływają na każdy wierzchołek siatki. Waga wpływu kości (skin weight) ma zwykle zakres 0-1. Suma aktywnych wag dla wierzchołka powinna być znormalizowana zgodnie z wymaganiami narzędzia eksportowego.

## Interpretacja wag

Waga 0 oznacza brak wpływu danej kości, 0,5 połowę wpływu w danym modelu mieszania, a 1 pełne związanie z kością. Nie oznacza to, że najlepsze deformacje uzyskuje się przez ostre granice 0/1. Strefy stawów wymagają kontrolowanego przejścia między kośćmi.

Zbyt wąskie przejście wag tworzy ostre załamanie. Zbyt szerokie powoduje gumowe rozciąganie i wpływ odległych kości.

## Bark

Bark testuj przy zgięciu i odwiedzeniu 45°, 90°, 120° i 150°. Obserwuj:

- objętość mięśnia naramiennego;
- kształt pachy;
- przejście szyja-obojczyk-bark;
- fałd pod pachą;
- ruch łopatki i obojczyka.

Fail: widoczna dziura w pachwinie barkowej, ostre zapadnięcie mięśnia lub wydłużenie ramienia.

## Łokieć

Testuj 45°, 90° i 130°. Strona zgięciowa powinna kompresować tkankę, a strona tylna zachować łagodny łuk. Nie akceptujemy „rury gumowej” bez lokalnego fałdu ani ostrego przecięcia objętości.

## Przedramię

Przy pronacji i supinacji około ±80° obserwuj rozkład skrętu. Jeżeli skóra tworzy spiralny artefakt, popraw kości skrętne lub wagi.

## Dłoń

Testuj każdy palec osobno i gesty zbiorcze. Szczególną uwagę zwróć na:

- kostki MCP;
- stawy PIP i DIP;
- opuszki;
- podstawę kciuka;
- błony międzypalcowe.

## Biodro i pachwina

Testuj zgięcie biodra 45°, 90° i 120°, odwiedzenie około 45° oraz głęboki przysiad. Pachwina nie może zapadać się do wnętrza ani rozciągać jak membrana.

## Kolano

Testuj 45°, 90° i 130°. Rzepka i przód kolana powinny zachować objętość, a tył kolana może tworzyć kontrolowany fałd kompresyjny.

## Twarz

W twarzy skinning dotyczy głównie kości żuchwy, oczu i ewentualnych kości pomocniczych. Testuj `jawOpen`, ruch boczny żuchwy, mruganie, spojrzenie i ich kombinacje z kształtami deformacyjnymi.

## Tolerancja wpływu odległych kości

Wierzchołek nie powinien mieć znaczącej wagi od kości, która anatomicznie nie może wpływać na dany region. Wartości rzędu 0,01-0,03 mogą pojawić się po automatycznym skinningu, ale powinny zostać ocenione i usunięte, jeśli powodują widoczny ruch.

## Test regresyjny

Po każdej zmianie wag odtwórz cały zestaw poz obowiązkowych. Poprawa barku nie może pogorszyć łokcia, neutralnej pozy ani deformacji ubrania.

## Definition of Done

Skinning jest zatwierdzony, gdy nie występuje zapadanie objętości, ostre fałdy, gumowe rozciąganie, wpływ odległych kości ani penetracje w typowym zakresie ruchu.