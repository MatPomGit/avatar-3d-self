import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'

const tabs = [
  ['start', 'Start'],
  ['pipeline', 'Pipeline'],
  ['tools', 'Narzędzia'],
  ['viewer', 'Model 3D'],
  ['setup', 'Uruchomienie'],
  ['quality', 'Kontrola jakości'],
]

const steps = [
  ['Przygotowanie zdjęć', 'Wykonaj serię ostrych, równomiernie oświetlonych zdjęć twarzy z wielu kierunków. Umieść materiał wejściowy w references/photos/raw.'],
  ['Rekonstrukcja 3D', 'Uruchom photogrammetry_pipeline.py lub scan_colmap.py lokalnie na stanowisku z COLMAP. Wyniki trafiają do source/scans/colmap_output.'],
  ['MetaHuman i geometria twarzy', 'Dopasuj MetaHuman do skanu, zapisz model bazowy w source/metahuman i wygeneruj manifest blendshape przez metahuman_processor.py.'],
  ['Blendshapes i korekty', 'Wykonaj korekty mimiki i asymetrii w Blenderze lub Unreal Engine. Skrypty facial_blendshape_sculpt.py i blendshape_generator.py wspierają ten etap.'],
  ['Tekstury PBR', 'Wygeneruj mapy diffuse, normal, roughness, metallic i AO za pomocą pbr_texture_processor.py, a następnie przygotuj materiały przez material_converter.py.'],
  ['Animacja i lip sync', 'Wypal animacje przez animation_baking.py. Opcjonalny pipeline Piper tworzy audio i dane synchronizacji ust.'],
  ['Eksport', 'Eksport do Unreal wykonuj przez ue_export_pipeline.py lub ue_export_fbx.py. Finalny FBX przechowuj w exports.'],
  ['Walidacja', 'Sprawdź geometrię, rig, blendshapes, materiały, animacje, clipping i zachowanie modelu w docelowym silniku.'],
]

const tools = [
  ['Python 3.11', 'Podstawowe środowisko skryptów repozytorium.', 'wymagane', 'https://www.python.org/downloads/release/python-31116/'],
  ['COLMAP', 'Fotogrametryczna rekonstrukcja geometrii ze zdjęć.', 'dla skanu', 'https://colmap.github.io/install.html'],
  ['Blender', 'Korekta geometrii, blendshapes i kontrola modelu.', 'zalecane', 'https://www.blender.org/download/'],
  ['Unreal Engine 5', 'MetaHuman, test animacji i finalny eksport.', 'dla MetaHuman', 'https://www.unrealengine.com/download'],
  ['MetaHuman', 'Rigowanie i dopracowanie cyfrowej postaci.', 'UE5', 'https://www.metahuman.com/create'],
  ['Piper TTS', 'Opcjonalne lokalne TTS i wejście dla lip sync.', 'opcjonalne', 'https://github.com/OHF-Voice/piper1-gpl'],
]

const commands = `git clone https://github.com/MatPomGit/avatar-3d-self.git
cd avatar-3d-self
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

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
    new FBXLoader().load(
      `${import.meta.env.BASE_URL}model/avatar_final.fbx`,
      (fbx) => {
        model = fbx
        fbx.scale.multiplyScalar(0.01)
        let triangles = 0
        let vertices = 0
        fbx.traverse((child) => {
          if (child.isMesh) {
            const count = child.geometry.attributes.position?.count || 0
            vertices += count
            triangles += child.geometry.index ? child.geometry.index.count / 3 : count / 3
          }
        })
        setStats({ triangles: Math.round(triangles), vertices })
        setStatus('Model gotowy')
        scene.add(fbx)
      },
      undefined,
      () => setStatus('Model FBX nie został jeszcze opublikowany.')
    )
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

function App() {
  const initialTab = tabs.some(([id]) => id === window.location.hash.slice(1)) ? window.location.hash.slice(1) : 'start'
  const [activeTab, setActiveTab] = useState(initialTab)

  useEffect(() => {
    const onHashChange = () => {
      const id = window.location.hash.slice(1)
      if (tabs.some(([tabId]) => tabId === id)) setActiveTab(id)
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const openTab = (id) => {
    setActiveTab(id)
    window.history.replaceState(null, '', `#${id}`)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand brand-button" onClick={() => openTab('start')}><span className="brand-mark">A3</span><span>avatar-3d-self</span></button>
        <nav className="desktop-nav" aria-label="Główna nawigacja">
          {tabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'nav-tab active' : 'nav-tab'} onClick={() => openTab(id)}>{label}</button>)}
          <a className="nav-github" href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">GitHub ↗</a>
        </nav>
      </header>

      <div className="mobile-tabs" aria-label="Nawigacja mobilna">
        {tabs.map(([id, label]) => <button key={id} className={activeTab === id ? 'mobile-tab active' : 'mobile-tab'} onClick={() => openTab(id)}>{label}</button>)}
      </div>

      <main className="tab-main">
        {activeTab === 'start' && <section className="tab-view home-view">
          <div className="home-copy">
            <div className="hero-badge">Open source · reproducible pipeline</div>
            <p className="eyebrow">Photogrammetry · MetaHuman · PBR · Animation</p>
            <h1>Realistyczny cyfrowy awatar 3D</h1>
            <p className="lead">Repozytorium prowadzi od materiału zdjęciowego przez rekonstrukcję i MetaHuman do animowalnego modelu gotowego do użycia w silniku 3D.</p>
            <div className="actions">
              <button className="button primary" onClick={() => openTab('pipeline')}>Zobacz pipeline</button>
              <button className="button" onClick={() => openTab('tools')}>Pobierz narzędzia</button>
            </div>
          </div>
          <div className="home-dashboard">
            <div className="metric"><strong>8</strong><span>etapów procesu</span></div>
            <div className="metric"><strong>FBX</strong><span>format wyjściowy</span></div>
            <div className="metric"><strong>UE5</strong><span>środowisko docelowe</span></div>
            <div className="flow-card"><span>Zdjęcia</span><b>→</b><span>COLMAP</span><b>→</b><span>MetaHuman</span><b>→</b><span>PBR</span><b>→</b><span>Animacja</span></div>
          </div>
        </section>}

        {activeTab === 'pipeline' && <section className="tab-view">
          <div className="page-heading"><p className="eyebrow">Procedura</p><h2>Pipeline produkcyjny</h2><p>Każdy etap ma jednoznaczny wynik wejściowy dla następnego kroku.</p></div>
          <div className="steps">{steps.map(([title, text], index) => <article className="step" key={title}><span className="step-number">{String(index + 1).padStart(2, '0')}</span><h3>{title}</h3><p>{text}</p></article>)}</div>
        </section>}

        {activeTab === 'tools' && <section className="tab-view">
          <div className="page-heading"><p className="eyebrow">Narzędzia</p><h2>Środowisko pracy</h2><p>Instaluj tylko narzędzia potrzebne do realizowanego etapu.</p></div>
          <div className="tool-grid">{tools.map(([name, role, tag, href]) => <a className="tool-card" href={href} key={name} target="_blank" rel="noreferrer"><div className="tool-card-top"><strong>{name}</strong><span className="tool-tag">{tag}</span></div><p>{role}</p><span className="tool-link">Oficjalna strona i pobieranie <b>↗</b></span></a>)}</div>
          <div className="info-strip"><strong>Minimalny start:</strong><span>Git + Python 3.11. COLMAP dodaj przed rekonstrukcją, a Unreal Engine przed pracą z MetaHuman.</span></div>
        </section>}

        {activeTab === 'viewer' && <section className="tab-view">
          <div className="page-heading"><p className="eyebrow">Podgląd</p><h2>Interaktywny model 3D</h2><p>Viewer Three.js wyświetli finalny FBX automatycznie po opublikowaniu artefaktu.</p></div>
          <Viewer />
        </section>}

        {activeTab === 'setup' && <section className="tab-view setup-view">
          <div className="page-heading"><p className="eyebrow">Start lokalny</p><h2>Uruchomienie repozytorium</h2><p>Najpierw przygotuj środowisko Python, a programy 3D instaluj zależnie od etapu.</p></div>
          <div className="setup-grid"><pre><code>{commands}</code></pre><div className="requirements"><div><strong>Python 3.11</strong><span>skrypty, geometria, PBR</span></div><div><strong>COLMAP</strong><span>rekonstrukcja</span></div><div><strong>Blender</strong><span>korekty geometrii</span></div><div><strong>Unreal Engine 5</strong><span>MetaHuman i eksport</span></div></div></div>
        </section>}

        {activeTab === 'quality' && <section className="tab-view">
          <div className="page-heading"><p className="eyebrow">Kontrola jakości</p><h2>Kryteria gotowego awatara</h2><p>Model można uznać za gotowy dopiero po sprawdzeniu geometrii, materiałów i animacji w środowisku docelowym.</p></div>
          <div className="checklist"><span>Geometria zachowuje proporcje twarzy</span><span>Rig i wymagane blendshapes działają</span><span>Brak clippingu przy skrajnych pozach</span><span>Tekstury PBR reagują poprawnie na światło</span><span>Animacje przechodzą płynnie</span><span>Lip sync jest zsynchronizowany z dźwiękiem</span><span>Model został sprawdzony w docelowym silniku</span></div>
        </section>}
      </main>

      <footer><div><strong>avatar-3d-self</strong><span>Realistyczny awatar 3D od zdjęć do silnika.</span></div><a href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">Repozytorium GitHub ↗</a></footer>
    </div>
  )
}

export default App
