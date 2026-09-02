# 12. Rig ciała

**Input:** zatwierdzony base mesh po topology freeze.  
**Editable output:** skeleton + control rig w scenie DCC.  
**Specification:** [Skeleton specification](../rigging/skeleton-specification.md).

## Cel etapu

Rig ciała ma zapewnić anatomicznie wiarygodny zakres ruchu, stabilną hierarchię kości i przewidywalne sterowanie IK/FK. Nie jest wystarczające samo automatyczne umieszczenie armature wewnątrz siatki. Kluczowe są joint centers, lokalne osie i relacja szkieletu do anatomii konkretnej osoby.

## Przygotowanie

1. Użyj zatwierdzonej siatki po topology freeze.
2. Ustal rest pose, najlepiej A-pose lub T-pose zgodną z resztą pipeline'u.
3. Zablokuj skalę obiektu i upewnij się, że scena ma poprawne jednostki.
4. Otwórz specyfikację nazewnictwa i hierarchii szkieletu.
5. Nie rozpoczynaj weight paintingu przed zatwierdzeniem pozycji kości.

## Procedura

### 1. Root i miednica

Utwórz `root` jako globalny węzeł transformacji. Nad nim nie powinny znajdować się kości deformacyjne. `pelvis/hips` umieść w centrum anatomicznym miednicy, tak aby rotacja nie powodowała nienaturalnego przesuwania tułowia.

### 2. Kręgosłup

Podziel kręgosłup na kilka segmentów odpowiadających miednicy, odcinkowi lędźwiowemu, piersiowemu i górnej części klatki. Nie rozkładaj kości w równych odstępach tylko geometrycznie. Ich położenie powinno wspierać naturalne zgięcie i rotację.

### 3. Szyja i głowa

Szyja powinna umożliwiać rozłożenie ruchu pomiędzy podstawę szyi i górne segmenty. Pivot głowy ustaw w regionie anatomicznie odpowiadającym połączeniu czaszki z kręgosłupem, a nie w środku geometrycznym głowy.

### 4. Obojczyki i barki

Clavicle powinny zaczynać się blisko mostka i kończyć w pobliżu stawu barkowego. Ich ruch jest niezbędny przy uniesieniu ręki powyżej poziomu barku. Nie próbuj zastąpić ruchu obręczy barkowej samą rotacją upper arm.

### 5. Ramiona i łokcie

Umieść joint center barku wewnątrz głowy kości ramiennej. Oś łokcia ustaw zgodnie z rzeczywistą płaszczyzną zgięcia. Jeżeli joint jest przesunięty zbyt daleko do przodu lub tyłu, weight painting nie naprawi deformacji bez artefaktów.

### 6. Przedramię i twist bones

Pronation/supination nie powinna być realizowana całą rotacją w jednym stawie nadgarstka. Rozłóż twist wzdłuż przedramienia przez twist bones albo odpowiedni mechanizm deformacji.

### 7. Nogi

Hip joint umieść w obrębie panewki, knee joint w osi zgięcia kolana, a ankle joint w okolicy stawu skokowego. Sprawdź pozycje w kilku widokach, nie tylko z przodu.

### 8. Stopy

Dodaj heel, ball/toe controls lub równoważny system umożliwiający heel strike, toe-off i foot roll. Dla runtime zachowaj osobną warstwę kości deformacyjnych i kontrolnych, jeśli system DCC tego wymaga.

### 9. IK/FK

Dla rąk i nóg skonfiguruj przełączanie IK/FK. IK powinno posiadać pole target dla stabilnej orientacji łokcia i kolana. Przełączenie IK/FK nie powinno powodować skoku pozycji kończyny.

### 10. Osie lokalne

Sprawdź osie lokalne wszystkich kości. Lewa i prawa strona powinny być spójne semantycznie. Niespójne roll angles są częstą przyczyną problemów przy retargetingu i eksporcie.

## Test przed skinningiem

Przed rozpoczęciem weight paintingu wykonaj test kości bez przywiązanej siatki:

- shoulder abduction 120°;
- arm forward 120°;
- elbow flexion 130°;
- pronation/supination;
- hip flexion 100°;
- squat;
- knee flexion 130°;
- ankle dorsiflexion i plantarflexion;
- head yaw/pitch/roll.

Sprawdź, czy pivoty zachowują się anatomicznie.

## Różnice anatomiczne zależne od płci i sylwetki

Rig bazowy pozostaje wspólny, ale ruch wtórny i rozkład deformacji muszą uwzględniać anatomię konkretnej osoby. Dla postaci kobiecej może być potrzebny dodatkowy rig piersi oraz długich włosów. Nie należy jednak kodować „męskich” lub „żeńskich” proporcji w szkielecie jako sztywnego stereotypu. Joint placement wynika z anatomii konkretnego modelu.

## Inspekcja w Avatar Studio

Po zapisaniu sceny wybierz etap 12 i **Run supported operation**. Raport Blender pozwoli potwierdzić liczbę armatures i bones, jednostki sceny oraz obecność oczekiwanej struktury. Raport nie zastępuje jeszcze pełnej walidacji semantycznej nazw i orientacji kości.

## Typowe błędy

### Łokieć obraca się po łuku zamiast zginać

Joint center lub bone roll są błędne. Popraw szkielet przed skinningiem.

### Bark zapada się już przy samym obrocie kości

Sprawdź położenie shoulder joint i clavicle. Później konieczny może być twist/deformation helper i corrective shapes, ale zły pivot powinien zostać naprawiony na tym etapie.

### Kolano odwraca się w IK

Pole target jest źle umieszczony albo łańcuch ma niejednoznaczną płaszczyznę zgięcia.

### Retargetowana animacja skręca kończyny

Najpierw sprawdź lokalne osie i rest pose, zanim zmienisz dane animacji.

## Validation

Rig przechodzi etap, gdy:

- hierarchia odpowiada specyfikacji;
- root, pelvis, spine, neck, head i kończyny mają logiczne pivoty;
- lokalne osie są spójne;
- IK/FK działa bez skoków;
- twist jest rozłożony tam, gdzie jest potrzebny;
- zakres ruchu przechodzi test bez anatomicznie niemożliwych pivotów;
- rest pose jest zapisana i wersjonowana.

## DoD

Skeleton i control rig są zatwierdzone jako stabilna baza skinningu, dłoni, twarzy i animacji. Po rozpoczęciu skinningu zmiana położenia kości deformacyjnej jest zmianą kontraktu i wymaga ponownej walidacji zależnych etapów.
