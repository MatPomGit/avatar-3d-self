import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'

const primaryTabs = [
  ['start', 'Projekt'],
  ['pipeline', 'Pipeline'],
  ['viewer', 'Model 3D'],
  ['tools', 'Narzędzia'],
  ['setup', 'Uruchomienie'],
]

const knowledgeTabs = [
  ['pbr', 'Tekstury PBR'],
  ['uv', 'Mapy UV'],
  ['blendshapes', 'Blendshapes'],
  ['quality', 'Kontrola jakości'],
]

const allTabs = [...primaryTabs, ...knowledgeTabs]

const steps = [
  ['Zdjęcia', 'Punktem wejściowym jest seria ostrych zdjęć twarzy wykonanych z wielu kierunków, przy możliwie stałym oświetleniu i bez poruszenia. Zdjęcia powinny pokrywać przód, profile, półprofile oraz górną i dolną część głowy, ponieważ brakujące obszary później tworzą dziury albo błędną geometrię. Ten etap nie tworzy jeszcze modelu 3D, tylko przygotowuje materiał, z którego będzie możliwa rekonstrukcja.', 'Zestaw zdjęć gotowy do fotogrametrii'],
  ['Rekonstrukcja', 'COLMAP wyszukuje te same charakterystyczne punkty na wielu zdjęciach i na tej podstawie oblicza położenie kamer oraz strukturę sceny. Najpierw powstaje rzadka chmura punktów, a następnie można wygenerować gęstszą rekonstrukcję i siatkę powierzchni. Wynik nadal wymaga kontroli, ponieważ włosy, uszy i gładkie fragmenty skóry często rekonstruują się gorzej niż dobrze teksturowane obszary twarzy.', 'Chmura punktów i wstępna siatka 3D'],
  ['Geometria', 'Surowa siatka po fotogrametrii zwykle ma zbyt dużo wielokątów, nieregularną topologię i lokalne artefakty. W Blenderze lub narzędziach MetaHuman należy oczyścić powierzchnię, zachować proporcje twarzy i doprowadzić topologię do formy nadającej się do animacji. W przypadku MetaHuman geometria skanu służy głównie jako wzorzec kształtu, do którego dopasowywana jest dobrze zorganizowana siatka bazowa.', 'Czysta i animowalna geometria'],
  ['Mapy UV', 'Model 3D trzeba rozłożyć na płaską reprezentację 2D, aby tekstury mogły być jednoznacznie przypisane do powierzchni. Tworzy się wyspy UV i szwy, a następnie kontroluje rozciąganie, gęstość texeli i położenie ważnych obszarów twarzy. Dobre UV sprawia, że np. tekstura ust trafia dokładnie na usta, a pieprzyk na policzku nie przesuwa się na nos.', 'Poprawna mapa UV dla tekstur'],
  ['Materiały PBR', 'Do modelu dodaje się zestaw map opisujących fizyczne właściwości powierzchni: kolor, normalne, chropowatość, metaliczność i ewentualnie AO lub wysokość. Każda mapa odpowiada za inną cechę, dlatego nie należy traktować ich jak zwykłych wariantów kolorystycznych. Dla skóry szczególnie ważne są Base Color, Normal i Roughness, ponieważ razem odpowiadają za kolor, drobne nierówności oraz sposób odbijania światła.', 'Materiał reagujący poprawnie na oświetlenie'],
  ['Mimika', 'Mimika twarzy wymaga przygotowania blendshapes i odpowiedniego riga. Blendshape zapisuje konkretną zmianę położenia wierzchołków, np. uniesienie kącików ust albo zamknięcie powieki, a rig obsługuje większe ruchy wynikające z kości i kontrolerów. Kilka blendshapes można mieszać jednocześnie, co pozwala odtwarzać uśmiech, mruganie, grymasy oraz kształty ust potrzebne do lip sync.', 'Zestaw sterowalnych ekspresji twarzy'],
  ['Eksport', 'Gotowy model należy wyeksportować razem z geometrią, szkieletem, materiałami i wymaganymi blendshapes. W tym projekcie podstawowym formatem wymiany jest FBX, ponieważ jest szeroko obsługiwany przez Blender i Unreal Engine. Po eksporcie trzeba sprawdzić, czy skala, orientacja osi, nazwy kości oraz morph targets nie zmieniły się w trakcie konwersji.', 'FBX gotowy do importu do silnika'],
  ['Walidacja', 'Ostatni etap polega na sprawdzeniu modelu w docelowym środowisku, a nie tylko w programie, w którym był tworzony. Należy obejrzeć geometrię z bliska, sprawdzić UV, materiały PBR, deformacje riga, blendshapes i animację ust. Model uznaje się za gotowy dopiero wtedy, gdy nie ma zauważalnych artefaktów i zachowuje się poprawnie w realnym oświetleniu oraz animacji.', 'Zweryfikowany awatar 3D'],
]

const tools = [
  ['Python 3.11', 'Środowisko dla skryptów automatyzujących przetwarzanie danych, geometrii i tekstur. W tym repozytorium Python spina kolejne etapy pipeline i pozwala uruchamiać przygotowane narzędzia bez ręcznego wykonywania powtarzalnych operacji.', 'wymagane', 'https://www.python.org/downloads/release/python-31116/'],
  ['COLMAP', 'Narzędzie do fotogrametrii. Na podstawie wielu zdjęć oblicza pozycje kamer i rekonstruuje przestrzenną strukturę twarzy, która później służy jako baza do dalszego modelowania.', 'rekonstrukcja', 'https://colmap.github.io/install.html'],
  ['Blender', 'Główne narzędzie do ręcznej kontroli siatki, topologii, UV, materiałów i blendshapes. Przydaje się również do sprawdzania eksportu FBX przed przeniesieniem modelu do silnika.', 'modelowanie', 'https://www.blender.org/download/'],
  ['Unreal Engine 5', 'Środowisko docelowe do MetaHuman, materiałów, animacji i oceny finalnego modelu. Pozwala zweryfikować wygląd postaci w rzeczywistym oświetleniu sceny oraz sprawdzić zachowanie riga i mimiki.', 'silnik 3D', 'https://www.unrealengine.com/download'],
  ['MetaHuman', 'System do przygotowania dobrze zrigowanej cyfrowej postaci o standardowej topologii twarzy. W projekcie może służyć jako baza, do której dopasowywany jest indywidualny kształt zeskanowanej twarzy.', 'twarz', 'https://www.metahuman.com/create'],
  ['Piper TTS', 'Opcjonalny lokalny syntezator mowy używany jako źródło audio do testów lip sync. Nie jest wymagany do wykonania samego modelu 3D.', 'opcjonalne', 'https://github.com/OHF-Voice/piper1-gpl'],
]

const pbrMaps = [
  ['Base Color', 'Opisuje właściwy kolor powierzchni bez cieni i połysków zapisanych na stałe.', 'Na twarzy znajdują się tu m.in. kolor skóry, ust, brwi, pieprzyki i zarost. Jeżeli do tej mapy zostaną wypalone mocne cienie, materiał będzie wyglądał nienaturalnie po zmianie oświetlenia.'],
  ['Normal', 'Zmienia sposób, w jaki światło reaguje na drobne nierówności powierzchni, bez dodawania nowych wielokątów.', 'Dzięki tej mapie gładka geometrycznie twarz może mieć widoczne pory, zmarszczki i drobne nierówności. Jeżeli kanał Y jest odwrócony, wypukłości mogą wyglądać jak wgłębienia.'],
  ['Roughness', 'Określa, jak szerokie i rozmyte są odbicia światła na powierzchni.', 'Niższa wartość daje bardziej gładką i błyszczącą skórę, wyższa bardziej matową. W praktyce czoło, nos i usta mogą mieć inną roughness niż policzki.'],
  ['Metallic', 'Określa, czy fragment materiału zachowuje się optycznie jak metal.', 'Dla ludzkiej skóry wartość powinna być praktycznie zerowa. Ta mapa ma sens dopiero dla metalowych dodatków, np. kolczyków, okularów lub elementów ubioru.'],
  ['Ambient Occlusion', 'Wzmacnia zacienienie w miejscach, do których światło pośrednie dociera słabiej.', 'Może delikatnie podkreślić nozdrza, okolice uszu i inne zagłębienia. Nie powinna jednak zastępować prawdziwych cieni generowanych przez oświetlenie silnika.'],
]

const commands = `git clone https://github.com/MatPomGit/avatar-3d-self.git
cd avatar-3d-self
python -m venv .venv

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# Linux / macOS
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev,geometry,vision]"`

function Viewer() {
  const containerRef = useRef(null)
  const [status, setStatus] = useState('Sprawdzanie modelu…')
  const [stats, setStats] = useState(null)
  useEffect(() => {
    const container = containerRef.current
    if (!container) return undefined
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x08111f)
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 440, 0.1, 1000)
    camera.position.set(0, 1.55, 2.7)
    camera.lookAt(0, 1.45, 0)
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(container.clientWidth, 440)
    container.appendChild(renderer.domElement)
    scene.add(new THREE.HemisphereLight(0xffffff, 0x22324b, 2.2))
    const key = new THREE.DirectionalLight(0xffffff, 2.5)
    key.position.set(3, 4, 3)
    scene.add(key)
    let model = null
    let frameId = 0
    new FBXLoader().load(`${import.meta.env.BASE_URL}model/avatar_final.fbx`, (fbx) => {
      model = fbx
      fbx.scale.multiplyScalar(0.01)
      let triangles = 0
      let vertices = 0
      fbx.traverse((child) => {
        if (!child.isMesh) return
        const count = child.geometry.attributes.position?.count || 0
        vertices += count
        triangles += child.geometry.index ? child.geometry.index.count / 3 : count / 3
      })
      setStats({ triangles: Math.round(triangles), vertices })
      setStatus('Model gotowy')
      scene.add(fbx)
    }, undefined, () => setStatus('Model FBX nie został jeszcze opublikowany.'))
    const animate = () => {
      frameId = requestAnimationFrame(animate)
      if (model) model.rotation.y += 0.0025
      renderer.render(scene, camera)
    }
    animate()
    const resize = () => {
      const width = container.clientWidth
      camera.aspect = width / 440
      camera.updateProjectionMatrix()
      renderer.setSize(width, 440)
    }
    window.addEventListener('resize', resize)
    return () => {
      cancelAnimationFrame(frameId)
      window.removeEventListener('resize', resize)
      renderer.dispose()
      renderer.domElement.remove()
    }
  }, [])
  return <div className="viewer-card"><div ref={containerRef} className="viewer-canvas" /><div className="viewer-meta"><strong>{status}</strong>{stats && <span>{stats.triangles.toLocaleString()} trójkątów · {stats.vertices.toLocaleString()} wierzchołków</span>}</div></div>
}

function PracticalExample({ label, title, children, visual }) {
  return <article className="example-card"><div className={`example-visual ${visual}`} aria-hidden="true" /><div><span>{label}</span><h3>{title}</h3><p>{children}</p></div></article>
}

function App() {
  const requested = window.location.hash.slice(1)
  const initialTab = allTabs.some(([id]) => id === requested) ? requested : 'start'
  const [activeTab, setActiveTab] = useState(initialTab)
  const [knowledgeOpen, setKnowledgeOpen] = useState(knowledgeTabs.some(([id]) => id === initialTab))

  useEffect(() => {
    const onHashChange = () => {
      const id = window.location.hash.slice(1)
      if (allTabs.some(([tabId]) => tabId === id)) {
        setActiveTab(id)
        setKnowledgeOpen(knowledgeTabs.some(([tabId]) => tabId === id))
      }
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const openTab = (id) => {
    setActiveTab(id)
    setKnowledgeOpen(knowledgeTabs.some(([tabId]) => tabId === id))
    window.history.replaceState(null, '', `#${id}`)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return <div className="app-shell">
    <header className="topbar">
      <button className="brand brand-button" onClick={() => openTab('start')}><span className="brand-mark">A3</span><span>avatar-3d-self</span></button>
      <nav className="desktop-nav" aria-label="Główna nawigacja">
        {primaryTabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'nav-tab active' : 'nav-tab'} onClick={() => openTab(id)}>{label}</button>)}
        <div className="knowledge-menu"><button className={knowledgeOpen ? 'nav-tab active' : 'nav-tab'} onClick={() => setKnowledgeOpen(!knowledgeOpen)}>Wiedza <span>⌄</span></button>{knowledgeOpen && <div className="knowledge-dropdown">{knowledgeTabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'active' : ''} onClick={() => openTab(id)}>{label}</button>)}</div>}</div>
        <a className="nav-github" href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">GitHub ↗</a>
      </nav>
    </header>

    <div className="mobile-tabs">{allTabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'mobile-tab active' : 'mobile-tab'} onClick={() => openTab(id)}>{label}</button>)}</div>

    <main className="tab-main">
      {activeTab === 'start' && <section className="tab-view project-home">
        <div className="project-hero"><div className="hero-copy"><span className="project-kicker">Otwarty pipeline tworzenia cyfrowej postaci</span><h1>Od zdjęć do realistycznego awatara 3D</h1><p>Projekt pokazuje kompletny proces tworzenia cyfrowej postaci na podstawie zdjęć. Obejmuje rekonstrukcję geometrii, przygotowanie UV i materiałów PBR, mimikę twarzy oraz eksport modelu do środowiska 3D. Celem jest nie tylko uzyskanie podobnego wyglądu, ale również przygotowanie modelu, który można poprawnie oświetlać, animować i przenosić między narzędziami.</p><div className="actions"><button className="button primary" onClick={() => openTab('viewer')}>Zobacz model 3D</button><button className="button" onClick={() => openTab('pipeline')}>Jak powstaje model</button></div><div className="project-meta"><span><strong>8</strong> etapów</span><span><strong>FBX</strong> format wyjściowy</span><span><strong>UE5</strong> środowisko docelowe</span></div></div><button className="model-preview" onClick={() => openTab('viewer')} aria-label="Otwórz model 3D"><div className="preview-head"><span className="mesh-half" /></div><strong>MODEL 3D</strong><span>FBX · PBR · mimika</span></button></div>
        <div className="project-flow"><div className="section-title"><span>Proces</span><h2>Jak powstaje model</h2></div><div className="flow-steps">{['Zdjęcia','Rekonstrukcja','Geometria','Tekstury','Mimika','Eksport'].map((name, i) => <button key={name} onClick={() => openTab('pipeline')}><b>{String(i + 1).padStart(2, '0')}</b><span>{name}</span></button>)}</div></div>
        <div className="knowledge-teasers"><div className="section-title"><span>Wiedza techniczna</span><h2>Szczegóły techniczne</h2></div><div className="teaser-grid"><button onClick={() => openTab('pbr')}><strong>Tekstury PBR</strong><span>Jak konkretne mapy zmieniają wygląd skóry i czym różnią się między silnikami.</span></button><button onClick={() => openTab('uv')}><strong>Mapy UV</strong><span>Jak tekstura 2D jest przypisywana do twarzy 3D i skąd biorą się rozciągnięcia.</span></button><button onClick={() => openTab('blendshapes')}><strong>Blendshapes</strong><span>Jak zapisuje się ruchy twarzy i jak z wielu prostych zmian powstaje mimika oraz lip sync.</span></button></div></div>
      </section>}

      {activeTab === 'pipeline' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Pipeline tworzenia awatara</h2><p>Każdy etap ma określony materiał wejściowy, konkretną operację i wynik, który przechodzi do następnego kroku. Dzięki temu pipeline można powtarzać, kontrolować i poprawiać bez zgadywania, na którym etapie powstał błąd.</p></div><div className="steps">{steps.map(([title, text, output], i) => <article className="step" key={title}><span className="step-number">{String(i + 1).padStart(2, '0')}</span><h3>{title}</h3><p>{text}</p><small>Wynik: {output}</small></article>)}</div></section>}

      {activeTab === 'viewer' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Rezultat projektu</p><h2>Interaktywny model 3D</h2><p>Viewer służy do szybkiej kontroli finalnego modelu bez uruchamiania Blendera lub Unreal Engine. Pozwala sprawdzić, czy plik FBX został poprawnie opublikowany, czy geometria się wczytuje oraz jak wygląda ogólna sylwetka modelu. Dokładna walidacja materiałów, riga i mimiki nadal powinna być wykonywana w środowisku docelowym.</p></div><Viewer /></section>}

      {activeTab === 'pbr' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Tekstury PBR</h2><p>PBR nie oznacza jednej tekstury, tylko zestaw map opisujących różne właściwości materiału. Silnik łączy te informacje z oświetleniem sceny, dzięki czemu ta sama skóra może wyglądać poprawnie zarówno w cieniu, jak i w mocnym świetle. Najważniejsze jest rozdzielenie koloru powierzchni od informacji o jej mikrogeometrii i sposobie odbijania światła.</p></div><div className="example-grid">{pbrMaps.map(([name, role, example]) => <PracticalExample key={name} label={name} title={role} visual={`visual-${name.toLowerCase().replaceAll(' ','-')}`}>{example}</PracticalExample>)}</div><div className="comparison-block"><div className="section-title"><span>Silniki</span><h2>Unity, Unreal Engine i Twinmotion</h2></div><div className="engine-compare"><div><strong>Unity</strong><p>W wielu standardowych shaderach Unity używana jest wartość Smoothness. Jest ona odwrotnością Roughness, więc mapę roughness trzeba odwrócić albo wykonać operację 1 − roughness w shaderze. Sposób pakowania kanałów zależy od używanego render pipeline.</p></div><div><strong>Unreal Engine</strong><p>Unreal Engine używa wejścia Roughness bezpośrednio. Osobno przyjmuje Base Color, Metallic i Normal, a dane skalarne można pakować do kanałów jednej tekstury. Dzięki temu łatwo zachować przewidywalny workflow PBR.</p></div><div><strong>Twinmotion</strong><p>Twinmotion również pracuje z Roughness. Przy mapach normalnych ważna jest konwencja DirectX lub OpenGL, ponieważ różnią się znakiem zielonego kanału. Jeżeli normal map wygląda odwrotnie, należy przełączyć odpowiednią opcję lub odwrócić kanał G.</p></div></div></div></section>}

      {activeTab === 'uv' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Mapy UV postaci</h2><p>Mapa UV jest sposobem przypisania punktów powierzchni modelu 3D do współrzędnych na płaskim obrazie 2D. U i V pełnią rolę dwóch osi tekstury, podobnie jak X i Y na zwykłym obrazie. Dzięki temu każdy wierzchołek modelu wie, z którego miejsca tekstury ma pobrać kolor i pozostałe dane materiałowe.</p></div><div className="demo-strip"><div className="uv-face">3D</div><span>rozcięcie</span><div className="uv-flat">UV</div><span>+ tekstura</span><div className="uv-result">gotowa twarz</div></div><div className="example-grid"><PracticalExample label="Przykład 1" title="Pieprzyk na policzku" visual="visual-uv-dot">Na teksturze pieprzyk znajduje się w konkretnym miejscu obrazu. Poprawne UV mapuje ten fragment dokładnie na policzek modelu. Jeżeli wyspa UV jest przesunięta lub obrócona, ten sam detal może pojawić się na nosie, uchu albo zupełnie poza twarzą.</PracticalExample><PracticalExample label="Przykład 2" title="Rozciągnięta tekstura" visual="visual-uv-stretch">Wyspa UV powinna możliwie wiernie odpowiadać proporcjom powierzchni modelu. Jeżeli policzek jest na UV zbyt mocno rozciągnięty, okrągły detal stanie się wydłużony. Takie zniekształcenie widać szczególnie dobrze na wzorach kontrolnych typu checker.</PracticalExample><PracticalExample label="Przykład 3" title="Szew z tyłu głowy" visual="visual-uv-seam">Nie da się rozłożyć zamkniętej powierzchni głowy na płasko bez wykonania cięć. Miejsca tych cięć nazywa się szwami UV. Umieszcza się je zwykle tam, gdzie będą najmniej widoczne, np. z tyłu głowy lub pod włosami.</PracticalExample><PracticalExample label="Przykład 4" title="Gęstość texeli" visual="visual-uv-density">Różne części twarzy powinny mieć sensowną ilość miejsca na teksturze. Jeżeli usta zajmują bardzo mały obszar UV, będą miały mniej szczegółów niż policzki. Dlatego ważne fragmenty twarzy dostają odpowiednio dużą rozdzielczość na mapie.</PracticalExample></div></section>}

      {activeTab === 'blendshapes' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Blendshapes mimiki twarzy</h2><p>Blendshape zapisuje różnicę między neutralną siatką twarzy a jej zmienioną wersją. Nie tworzy osobnego modelu, tylko informację, które wierzchołki mają się przesunąć i o ile. Dzięki temu jedną siatkę można płynnie deformować od stanu neutralnego do uśmiechu, mrugnięcia albo otwarcia ust.</p></div><div className="blend-demo"><div className="face neutral"><span>neutralna</span></div><div className="blend-slider"><span>0</span><div><i /></div><span>100</span></div><div className="face smile"><span>uśmiech</span></div></div><div className="example-grid"><PracticalExample label="Przykład 1" title="Uśmiech" visual="visual-smile">Tworzona jest wersja siatki, w której kąciki ust są przesunięte do góry i na zewnątrz. Przy wadze 0 twarz pozostaje neutralna, a przy pełnej wadze osiąga zapisany uśmiech. Wartości pośrednie tworzą płynne przejście między tymi stanami.</PracticalExample><PracticalExample label="Przykład 2" title="Mrugnięcie" visual="visual-blink">Blendshape może przesunąć wierzchołki górnej i dolnej powieki tak, aby zamknąć oko. Lewa i prawa strona powinny być sterowane osobno, ponieważ człowiek może mrugać niesymetrycznie. To samo podejście wykorzystuje się do unoszenia brwi i ruchu kącików ust.</PracticalExample><PracticalExample label="Przykład 3" title="Mieszanie ekspresji" visual="visual-mix">W praktyce twarz rzadko używa jednego blendshape naraz. Uśmiech może być połączony z lekkim zmrużeniem oczu i uniesieniem brwi. Końcowy kształt powstaje jako kombinacja wag wielu blendshapes działających jednocześnie.</PracticalExample><PracticalExample label="Przykład 4" title="Lip sync" visual="visual-lips">System synchronizacji ust zmienia w czasie wagi blendshapes odpowiadających za kształty ust i szczęki. Na podstawie dźwięku lub fonemów wybierane są kolejne ustawienia potrzebne do wymowy. Dzięki temu model nie odtwarza jednej animacji, tylko na bieżąco składa ruch ust z prostych deformacji.</PracticalExample></div></section>}

      {activeTab === 'tools' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Narzędzia</h2><p>Nie wszystkie programy są potrzebne jednocześnie. Zestaw zależy od etapu pipeline: COLMAP służy do rekonstrukcji, Blender do pracy na modelu, a Unreal Engine do MetaHuman, animacji i walidacji. Python automatyzuje operacje powtarzalne i łączy poszczególne etapy projektu.</p></div><div className="tool-grid">{tools.map(([name, role, tag, href]) => <a className="tool-card" href={href} key={name} target="_blank" rel="noreferrer"><div className="tool-card-top"><strong>{name}</strong><span className="tool-tag">{tag}</span></div><p>{role}</p><span className="tool-link">Oficjalna strona <b>↗</b></span></a>)}</div></section>}

      {activeTab === 'setup' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Uruchomienie repozytorium</h2><p>Najpierw przygotuj środowisko Python i zależności projektu. Programy zewnętrzne, takie jak COLMAP, Blender i Unreal Engine, instaluj dopiero wtedy, gdy są potrzebne do konkretnego etapu. Dzięki temu podstawowe środowisko pozostaje małe i łatwe do odtworzenia.</p></div><div className="setup-grid"><pre><code>{commands}</code></pre><div className="requirements"><div><strong>Python 3.11</strong><span>skrypty projektu i automatyzacja</span></div><div><strong>COLMAP</strong><span>fotogrametria i rekonstrukcja</span></div><div><strong>Blender</strong><span>geometria, UV i blendshapes</span></div><div><strong>Unreal Engine 5</strong><span>MetaHuman, animacja i walidacja</span></div></div></div></section>}

      {activeTab === 'quality' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Kontrola jakości</h2><p>Gotowy model trzeba oceniać jako całość, ponieważ błąd jednego etapu często ujawnia się dopiero później. Poprawna geometria nie wystarczy, jeżeli UV rozciąga tekstury albo blendshape powoduje zapadanie policzka. Najlepiej sprawdzać model po każdym większym etapie i ponownie po imporcie do środowiska docelowego.</p></div><div className="checklist"><span>Geometria zachowuje proporcje twarzy i nie zawiera widocznych artefaktów</span><span>UV nie powoduje przesunięć ani rozciągnięć tekstur</span><span>Materiały PBR reagują poprawnie na różne warunki oświetleniowe</span><span>Blendshapes zachowują naturalny kształt twarzy przy wartościach pośrednich i skrajnych</span><span>Rig nie powoduje nienaturalnych deformacji podczas ruchu</span><span>Lip sync odpowiada rytmowi i kształtom ust potrzebnym do wypowiedzi</span><span>Eksport FBX zachowuje skalę, orientację, kości, materiały i morph targets</span></div></section>}
    </main>

    <footer><div><strong>avatar-3d-self</strong><span>Od zdjęć do animowanej postaci 3D.</span></div><a href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">Repozytorium GitHub ↗</a></footer>
  </div>
}

export default App
