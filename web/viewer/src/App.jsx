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
  ['Zdjęcia', 'Zrób ostre zdjęcia twarzy z wielu kierunków.', 'Materiał wejściowy'],
  ['Rekonstrukcja', 'COLMAP odtwarza kształt twarzy ze zdjęć.', 'Chmura punktów i siatka'],
  ['Geometria', 'Oczyść siatkę i dopasuj model bazowy lub MetaHuman.', 'Poprawna topologia'],
  ['UV', 'Rozłóż powierzchnię modelu na płaskiej mapie.', 'Miejsce dla tekstur'],
  ['PBR', 'Dodaj kolor skóry, normal, roughness i pozostałe mapy.', 'Realistyczny materiał'],
  ['Mimika', 'Przygotuj blendshapes i rig twarzy.', 'Uśmiech, mruganie, mowa'],
  ['Eksport', 'Zapisz gotową postać do formatu FBX.', 'Model do silnika 3D'],
  ['Walidacja', 'Sprawdź model, materiały i animację w środowisku docelowym.', 'Gotowy awatar'],
]

const tools = [
  ['Python 3.11', 'Skrypty projektu i przetwarzanie danych.', 'wymagane', 'https://www.python.org/downloads/release/python-31116/'],
  ['COLMAP', 'Rekonstrukcja geometrii 3D ze zdjęć.', 'rekonstrukcja', 'https://colmap.github.io/install.html'],
  ['Blender', 'Geometria, UV, materiały i blendshapes.', 'modelowanie', 'https://www.blender.org/download/'],
  ['Unreal Engine 5', 'MetaHuman, materiały, animacja i test modelu.', 'silnik 3D', 'https://www.unrealengine.com/download'],
  ['MetaHuman', 'Rig i dopracowanie cyfrowej postaci.', 'twarz', 'https://www.metahuman.com/create'],
  ['Piper TTS', 'Opcjonalny głos wejściowy do lip sync.', 'opcjonalne', 'https://github.com/OHF-Voice/piper1-gpl'],
]

const pbrMaps = [
  ['Base Color', 'Kolor skóry bez cieni i połysku.', 'Na twarz trafia np. kolor ust, pieprzyki i zarost.'],
  ['Normal', 'Udaje drobne nierówności bez dodawania geometrii.', 'Pory skóry mogą być widoczne mimo gładkiej siatki.'],
  ['Roughness', 'Steruje tym, jak mocno powierzchnia odbija światło.', 'Czoło może być bardziej błyszczące niż policzek.'],
  ['Metallic', 'Określa, czy powierzchnia zachowuje się jak metal.', 'Dla skóry zwykle 0, dla metalowych dodatków 1.'],
  ['AO', 'Przyciemnia miejsca, do których światło dociera słabiej.', 'Pomaga podkreślić okolice nozdrzy i zagłębienia.'],
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
        <div className="knowledge-menu">
          <button className={knowledgeOpen ? 'nav-tab active' : 'nav-tab'} onClick={() => setKnowledgeOpen(!knowledgeOpen)}>Wiedza <span>⌄</span></button>
          {knowledgeOpen && <div className="knowledge-dropdown">{knowledgeTabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'active' : ''} onClick={() => openTab(id)}>{label}</button>)}</div>}
        </div>
        <a className="nav-github" href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">GitHub ↗</a>
      </nav>
    </header>

    <div className="mobile-tabs">{allTabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'mobile-tab active' : 'mobile-tab'} onClick={() => openTab(id)}>{label}</button>)}</div>

    <main className="tab-main">
      {activeTab === 'start' && <section className="tab-view project-home">
        <div className="project-hero">
          <div className="hero-copy">
            <span className="project-kicker">Otwarty pipeline tworzenia cyfrowej postaci</span>
            <h1>Od zdjęć do realistycznego awatara 3D</h1>
            <p>Projekt prowadzi przez rekonstrukcję twarzy, przygotowanie geometrii, materiałów, mimiki i eksport modelu do silnika 3D.</p>
            <div className="actions"><button className="button primary" onClick={() => openTab('viewer')}>Zobacz model 3D</button><button className="button" onClick={() => openTab('pipeline')}>Jak powstaje model</button></div>
            <div className="project-meta"><span><strong>8</strong> etapów</span><span><strong>FBX</strong> format wyjściowy</span><span><strong>UE5</strong> środowisko docelowe</span></div>
          </div>
          <button className="model-preview" onClick={() => openTab('viewer')} aria-label="Otwórz model 3D"><div className="preview-head"><span className="mesh-half" /></div><strong>MODEL 3D</strong><span>FBX · PBR · mimika</span></button>
        </div>

        <div className="project-flow"><div className="section-title"><span>Proces</span><h2>Jak powstaje model</h2></div><div className="flow-steps">{['Zdjęcia','Rekonstrukcja','Geometria','Tekstury','Mimika','Eksport'].map((name, i) => <button key={name} onClick={() => openTab('pipeline')}><b>{String(i + 1).padStart(2, '0')}</b><span>{name}</span></button>)}</div></div>

        <div className="knowledge-teasers"><div className="section-title"><span>Wiedza techniczna</span><h2>Szczegóły dopiero wtedy, gdy są potrzebne</h2></div><div className="teaser-grid"><button onClick={() => openTab('pbr')}><strong>Tekstury PBR</strong><span>Przykład: gdzie podłączyć roughness i normal map.</span></button><button onClick={() => openTab('uv')}><strong>Mapy UV</strong><span>Przykład: jak kolor policzka trafia dokładnie na policzek modelu.</span></button><button onClick={() => openTab('blendshapes')}><strong>Blendshapes</strong><span>Przykład: co dokładnie robi suwak „uśmiech”.</span></button></div></div>
      </section>}

      {activeTab === 'pipeline' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Pipeline tworzenia awatara</h2><p>Każdy etap daje konkretny wynik potrzebny w następnym kroku.</p></div><div className="steps">{steps.map(([title, text, output], i) => <article className="step" key={title}><span className="step-number">{String(i + 1).padStart(2, '0')}</span><h3>{title}</h3><p>{text}</p><small>Wynik: {output}</small></article>)}</div></section>}

      {activeTab === 'viewer' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Rezultat projektu</p><h2>Interaktywny model 3D</h2><p>To tutaj ma być oglądany finalny awatar. Viewer wczytuje opublikowany model FBX.</p></div><Viewer /></section>}

      {activeTab === 'pbr' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Tekstury PBR na konkretnym przykładzie</h2><p>Zamiast traktować mapy jak abstrakcyjne pliki, zobacz co każda z nich zmienia na twarzy.</p></div><div className="example-grid">{pbrMaps.map(([name, role, example]) => <PracticalExample key={name} label={name} title={role} visual={`visual-${name.toLowerCase().replaceAll(' ','-')}`}>{example}</PracticalExample>)}</div><div className="comparison-block"><div className="section-title"><span>Silniki</span><h2>Najważniejsza różnica</h2></div><div className="engine-compare"><div><strong>Unity</strong><p>Często używa Smoothness. Jeżeli masz Roughness, zwykle trzeba ją odwrócić.</p></div><div><strong>Unreal Engine</strong><p>Używa Roughness bezpośrednio.</p></div><div><strong>Twinmotion</strong><p>Także używa Roughness. Mapę normalną można przełączyć między DirectX i OpenGL.</p></div></div></div></section>}

      {activeTab === 'uv' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Mapy UV postaci</h2><p>UV odpowiada na jedno pytanie: który fragment obrazka ma trafić w które miejsce modelu?</p></div><div className="demo-strip"><div className="uv-face">3D</div><span>rozcięcie</span><div className="uv-flat">UV</div><span>+ tekstura</span><div className="uv-result">gotowa twarz</div></div><div className="example-grid"><PracticalExample label="Przykład 1" title="Pieprzyk na policzku" visual="visual-uv-dot">Jeżeli współrzędne UV są poprawne, pieprzyk z tekstury pojawia się dokładnie na policzku. Gdy UV jest przesunięte, pieprzyk może trafić na nos albo ucho.</PracticalExample><PracticalExample label="Przykład 2" title="Rozciągnięta tekstura" visual="visual-uv-stretch">Okrągły szczegół powinien pozostać okrągły. Jeżeli wygląda jak długa plama, wyspa UV jest rozciągnięta.</PracticalExample><PracticalExample label="Przykład 3" title="Szew z tyłu głowy" visual="visual-uv-seam">Model trzeba gdzieś rozciąć, aby rozłożyć go na płasko. Szew umieszcza się tam, gdzie będzie najmniej widoczny.</PracticalExample></div><div className="info-strip"><strong>W skrócie:</strong><span>UV nie zmienia kształtu modelu. To instrukcja przyklejenia obrazu 2D do powierzchni 3D.</span></div></section>}

      {activeTab === 'blendshapes' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Blendshapes mimiki twarzy</h2><p>Blendshape zapisuje, jak konkretne wierzchołki twarzy mają się przesunąć.</p></div><div className="blend-demo"><div className="face neutral">neutralna</div><div className="weight"><span>0</span><div><i /></div><span>100</span></div><div className="face smile">uśmiech</div></div><div className="example-grid"><PracticalExample label="Uśmiech" title="Kąciki ust idą w górę" visual="visual-smile">Program nie podmienia całej głowy. Przesuwa tylko zapisane wierzchołki. Wartość 0 daje twarz neutralną, a 100 pełny uśmiech.</PracticalExample><PracticalExample label="Mrugnięcie" title="Powieka zamyka oko" visual="visual-blink">Osobny blendshape może sterować lewym i prawym okiem. Dzięki temu postać może mrugać niezależnie.</PracticalExample><PracticalExample label="Mowa" title="Kilka kształtów ust naraz" visual="visual-mouth">Lip sync zmienia w czasie wagi kilku blendshapes. Z ich mieszania powstają kształty ust odpowiadające mowie.</PracticalExample></div><div className="info-strip"><strong>W skrócie:</strong><span>Kość porusza większym fragmentem modelu. Blendshape precyzyjnie przesuwa zapisane wierzchołki i dlatego dobrze nadaje się do mimiki.</span></div></section>}

      {activeTab === 'tools' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Narzędzia</h2><p>Instaluj tylko narzędzia potrzebne na aktualnym etapie.</p></div><div className="tool-grid">{tools.map(([name, role, tag, href]) => <a className="tool-card" href={href} key={name} target="_blank" rel="noreferrer"><div className="tool-card-top"><strong>{name}</strong><span className="tool-tag">{tag}</span></div><p>{role}</p><span className="tool-link">Oficjalna strona <b>↗</b></span></a>)}</div></section>}

      {activeTab === 'setup' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Projekt</p><h2>Uruchomienie repozytorium</h2><p>Minimalny start to Git i Python 3.11. Narzędzia 3D dodawaj dopiero wtedy, gdy są potrzebne.</p></div><div className="setup-grid"><pre><code>{commands}</code></pre><div className="requirements"><div><strong>Python 3.11</strong><span>skrypty</span></div><div><strong>COLMAP</strong><span>rekonstrukcja</span></div><div><strong>Blender</strong><span>geometria, UV i blendshapes</span></div><div><strong>Unreal Engine 5</strong><span>MetaHuman i eksport</span></div></div></div></section>}

      {activeTab === 'quality' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Wiedza techniczna</p><h2>Kiedy model jest gotowy?</h2><p>Sprawdź rezultat w praktyce, nie tylko pliki w katalogu.</p></div><div className="checklist"><span>Twarz ma poprawne proporcje</span><span>Tekstura trafia w poprawne miejsca UV</span><span>Materiały PBR reagują poprawnie na światło</span><span>Blendshapes nie deformują twarzy</span><span>Rig i animacje działają</span><span>Lip sync pasuje do głosu</span><span>Model działa w docelowym silniku</span></div></section>}
    </main>

    <footer><div><strong>avatar-3d-self</strong><span>Od zdjęć do animowanej postaci 3D.</span></div><a href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">Repozytorium GitHub ↗</a></footer>
  </div>
}

export default App
