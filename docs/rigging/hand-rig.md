# Układ sterowania dłonią

Dłoń zawiera wiele niewielkich stawów, których deformacje są bardzo widoczne w zbliżeniu i podczas gestykulacji. Rig dłoni powinien umożliwiać zarówno szybkie sterowanie całym gestem, jak i niezależną korektę każdego palca.

## Łańcuchy palców

Każdy palec ma niezależny łańcuch deformacyjny. Dla palców II-V wymagane są co najmniej stawy odpowiadające MCP, PIP i DIP. Kciuk wymaga osobnej orientacji podstawy oraz możliwości opozycji.

## Zgięcie palców

Wartość sterownika `curl` można normalizować do zakresu 0-1:

- 0,0: dłoń otwarta;
- 0,25: lekkie zgięcie;
- 0,5: chwyt luźny;
- 0,75: silne zgięcie;
- 1,0: pełna pięść lub maksymalny zatwierdzony zakres.

Nie należy rozdzielać tej wartości równomiernie między wszystkie stawy. W naturalnym zaciskaniu dłoni stawy MCP, PIP i DIP mają różny udział, a proporcje zależą od palca.

## Rozstaw palców

Sterownik `spread` odpowiada za odwodzenie i przywodzenie palców. Typowy zakres roboczy jest niewielki. Nadmierny rozstaw prowadzi do nienaturalnego wachlarza dłoni i rozciągania błon międzypalcowych.

## Kciuk i opozycja

Opozycja kciuka jest ruchem złożonym. Nie jest prostym zgięciem jednego stawu. Powinna łączyć rotację u podstawy, odwiedzenie i zgięcie.

Testy obowiązkowe:

- dotknięcie opuszki wskaziciela;
- dotknięcie opuszki małego palca;
- chwyt cylindryczny;
- chwyt szczypcowy.

## Łuki dłoni

Naturalna dłoń nie jest płaską płytą. Podczas chwytu śródręcze tworzy łuk poprzeczny i podłużny. Rig powinien umożliwiać subtelne złożenie dłoni, szczególnie po stronie małego palca.

## Kontrolery zbiorcze

Zalecane sterowniki:

- `fist`;
- `curl` per palec;
- `spread`;
- `thumb_opposition`;
- `cup` dla łuku dłoni.

Każdy sterownik zbiorczy musi pozostawiać możliwość ręcznej korekty pojedynczego stawu.

## Walidacja

Testuj:

1. otwartą dłoń;
2. pełną pięść;
3. wskazywanie;
4. gest szczypcowy;
5. chwyt cylindryczny;
6. chwyt sferyczny;
7. opozycję kciuka;
8. kontakt z rzeczywistym rekwizytem.

Błąd występuje, gdy:

- kostki palców zapadają się;
- opuszki tracą objętość;
- błony międzypalcowe rozrywają się lub sklejają;
- paznokcie odrywają się od geometrii palca;
- palce przecinają się przy typowych chwytach.

## Definition of Done

Dłoń jest zatwierdzona, gdy wszystkie palce działają niezależnie, gesty zbiorcze są naturalne, kciuk osiąga opozycję bez penetracji, a deformacja zachowuje objętość opuszek i kostek.