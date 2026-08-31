import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'

const steps = [
  ['1. Przygotowanie zdjęć', 'Wykonaj serię ostrych, równomiernie oświetlonych zdjęć twarzy z wielu kierunków. Umieść materiał wejściowy w references/photos/raw.'],
  ['2. Rekonstrukcja 3D', 'Uruchom photogrammetry_pipeline.py lub scan_colmap.py lokalnie na stanowisku z COLMAP. Wyniki rekonstrukcji trafiają do source/scans/colmap_output.'],
  ['3. MetaHuman i geometria twarzy', 'Dopasuj MetaHuman do skanu, zapisz bazowy model w source/metahuman i wygeneruj manifest blendshape przez metahuman_processor.py.'],
  ['4. Blendshapes i korekty', 'Wykonaj korekty mimiki i asymetrii w Blenderze lub Unreal Engine. Skrypty facial_blendshape_sculpt.py i blendshape_generator.py wspierają ten etap.'],
  ['5. Tekstury PBR', 'Wygeneruj mapy diffuse, normal, roughness, metallic i AO za pomocą pbr_texture_processor.py, a następnie przygotuj materiały przez material_converter.py.'],
  ['6. Animacja i lip sync', 'Wypal animacje przez animation_baking.py. Opcjonalny pipeline Piper tworzy audio i dane synchronizacji ust w piper_lipsync_generator.py.'],
  ['7. Eksport', 'Eksport do Unreal wykonuj w środowisku Unreal Engine przez ue_export_pipeline.py lub ue_export_fbx.py. Finalny FBX przechowuj w exports.'],
  ['8. Walidacja', 'Sprawdź geometrię, rig, blendshapes, materiały, animacje, brak clippingu i zachowanie modelu w docelowym silniku.'],
]

const tools = [
  {
    name: 'Python 3.11',
    role: 'Podstawowe środowisko skryptów i narzędzi repozytorium.',
    tag: 'wymagane',
    href: 'https://www.python.org/downloads/release/python-31116/',
  },
  {
    name: 'COLMAP',
    role: 'Fotogrametryczna rekonstrukcja geometrii z serii zdjęć.',
    tag: 'wymagane dla skanu',
    href: 'https://colmap.github.io/install.html',
  },
  {
    name: 'Blender',
    role: 'Korekta geometrii, asymetrii, blendshapes i kontrola modelu.',
    tag: 'zalecane',
    href: 'https://www.blender.org/download/',
  },
  {
    name: 'Unreal Engine 5',
    role: 'Środowisko MetaHuman, test animacji i finalny eksport.',
    tag: 'wymagane dla MetaHuman',
    href: 'https://www.unrealengine.com/download',
  },
  {
    name: 'MetaHuman',
    role: 'Mesh to MetaHuman, rigowanie oraz dopracowanie cyfrowej postaci.',
    tag: 'część Unreal Engine',
    href: 'https://www.metahuman.com/create',
  },
  {
    name: 'Piper TTS',
    role: 'Opcjonalne lokalne TTS oraz dane wejściowe dla lip sync.',
    tag: 'opcjonalne',
    href: 'https://github.com/OHF-Voice/piper1-gpl',
  },
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

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 420, 0.1, 1000)
    camera.position.set(0, 1.55, 2.7)
    camera.lookAt(0, 1.45, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(container.clientWidth, 420)
    container.appendChild(renderer.domElement)

    scene.add(new THREE.HemisphereLight(0xffffff, 0x22324b, 2.2))
    const key = new THREE.DirectionalLight(0xffffff, 2.5)
    key.position.set(3, 4, 3)
    scene.add(key)

    let model = null
    let frameId = 0
    const loader = new FBXLoader()
    const modelUrl = `${import.meta.env.BASE_URL}model/avatar_final.fbx`

    loader.load(
      modelUrl,
      (fbx) => {
        model = fbx
        fbx.scale.multiplyScalar(0.01)
        let triangles = 0
        let vertices = 0
        fbx.traverse((child) => {
          if (child.isMesh) {
            vertices += child.geometry.attributes.position?.count || 0
            triangles += child.geometry.index ? child.geometry.index.count / 3 : vertices / 3
          }
        })
        setStats({ triangles: Math.round(triangles), vertices })
        setStatus('Model gotowy')
        scene.add(fbx)
      },
      undefined,
      () => setStatus('Model FBX nie został jeszcze opublikowany. Dokumentacja jest dostępna niezależnie od modelu.')
    )

    const animate = () => {
      frameId = requestAnimationFrame(animate)
      if (model) model.rotation.y += 0.0025
      renderer.render(scene, camera)
    }
    animate()

    const resize = () => {
      const width = container.clientWidth
      camera.aspect = width / 420
      camera.updateProjectionMatrix()
      renderer.setSize(width, 420)
    }
    window.addEventListener('resize', resize)

    return () => {
      cancelAnimationFrame(frameId)
      window.removeEventListener('resize', resize)
      renderer.dispose()
      renderer.domElement.remove()
    }
  }, [])

  return (
    <section id="viewer" className="section">
      <div className="section-heading compact-heading">
        <p className="eyebrow">Podgląd</p>
        <h2>Interaktywny model 3D</h2>
        <p>Viewer wykorzystuje Three.js i automatycznie wyświetli finalny plik FBX, gdy artefakt zostanie opublikowany razem ze stroną.</p>
      </div>
      <div className="viewer-card">
        <div ref={containerRef} className="viewer-canvas" />
        <div className="viewer-meta">
          <strong>{status}</strong>
          {stats && <span>{stats.triangles.toLocaleString()} trójkątów · {stats.vertices.toLocaleString()} wierzchołków</span>}
        </div>
      </div>
    </section>
  )
}

function App() {
  return (
    <div>
      <header className="topbar">
        <a className="brand" href="#start"><span className="brand-mark">A3</span><span>avatar-3d-self</span></a>
        <nav>
          <a href="#about">Projekt</a>
          <a href="#pipeline">Pipeline</a>
          <a href="#tools">Narzędzia</a>
          <a href="#viewer">3D</a>
          <a href="#setup">Uruchomienie</a>
          <a className="nav-github" href="https://github.com/MatPomGit/avatar-3d-self">GitHub ↗</a>
        </nav>
      </header>

      <main>
        <section id="start" className="hero">
          <div className="hero-copy">
            <div className="hero-badge">Open source · reproducible pipeline</div>
            <p className="eyebrow">Photogrammetry · MetaHuman · PBR · Animation</p>
            <h1>Realistyczny cyfrowy awatar 3D z pełnym pipeline’em produkcyjnym</h1>
            <p className="lead">Projekt łączy rekonstrukcję fotogrametryczną, przetwarzanie geometrii i tekstur, MetaHuman, blendshapes, animację, lip sync oraz eksport do silników 3D. Ta strona jest jednocześnie opisem projektu i instrukcją jego odtworzenia.</p>
            <div className="actions">
              <a className="button primary" href="#pipeline">Zobacz cały proces</a>
              <a className="button" href="#tools">Pobierz narzędzia</a>
            </div>
            <div className="hero-facts">
              <span><strong>8</strong> etapów</span>
              <span><strong>FBX</strong> format wyjściowy</span>
              <span><strong>UE5</strong> środowisko docelowe</span>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-panel">
              <span>Wejście</span><strong>Zdjęcia wielowidokowe</strong>
              <span>Rekonstrukcja</span><strong>COLMAP + mesh</strong>
              <span>Awatar</span><strong>MetaHuman + blendshapes</strong>
              <span>Wygląd</span><strong>PBR + materiały</strong>
              <span>Ruch</span><strong>Animacja + lip sync</strong>
              <span>Wyjście</span><strong>FBX / Unreal / Unity</strong>
            </div>
            <div className="hero-caption">Od surowych zdjęć do gotowej, animowalnej postaci 3D.</div>
          </div>
        </section>

        <section id="about" className="section split about-section">
          <div className="section-heading">
            <p className="eyebrow">Cel</p>
            <h2>Jeden repozytoryjny przepływ od zdjęć do awatara</h2>
          </div>
          <div className="prose surface-copy">
            <p>Repozytorium porządkuje narzędzia potrzebne do zbudowania realistycznego awatara człowieka. Python odpowiada za etapy możliwe do automatyzacji, natomiast COLMAP, Blender i Unreal Engine pozostają środowiskami wykonawczymi dla zadań wymagających natywnych narzędzi 3D.</p>
            <p>GitHub Actions wykonuje lekką walidację kodu i publikuje tę stronę. Ciężka fotogrametria i eksport Unreal nie są uruchamiane na standardowym runnerze GitHub.</p>
          </div>
        </section>

        <section id="pipeline" className="section">
          <div className="section-heading">
            <p className="eyebrow">Procedura</p>
            <h2>Kompletny pipeline</h2>
            <p>Kolejność odpowiada zależnościom między danymi. Etapy 2, 4 i 7 wymagają lokalnych narzędzi 3D.</p>
          </div>
          <div className="steps">
            {steps.map(([title, text], index) => (
              <article className="step" key={title}>
                <span className="step-number">{String(index + 1).padStart(2, '0')}</span>
                <h3>{title.replace(/^\d+\.\s*/, '')}</h3>
                <p>{text}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="tools" className="section tools-section">
          <div className="section-heading">
            <p className="eyebrow">Narzędzia</p>
            <h2>Pobierz środowisko pracy</h2>
            <p>Linki prowadzą do oficjalnych stron projektów. Nie wszystkie narzędzia są potrzebne na każdym etapie.</p>
          </div>
          <div className="tool-grid">
            {tools.map((tool) => (
              <a className="tool-card" href={tool.href} key={tool.name} target="_blank" rel="noreferrer">
                <div className="tool-card-top">
                  <strong>{tool.name}</strong>
                  <span className="tool-tag">{tool.tag}</span>
                </div>
                <p>{tool.role}</p>
                <span className="tool-link">Oficjalna strona / pobieranie <b>↗</b></span>
              </a>
            ))}
          </div>
          <div className="tool-note">
            <strong>Minimalny zestaw do rozpoczęcia:</strong>
            <span>Python 3.11 + Git. COLMAP jest potrzebny do rekonstrukcji, a Unreal Engine do etapu MetaHuman i eksportu.</span>
          </div>
        </section>

        <Viewer />

        <section id="setup" className="section split setup-section">
          <div className="section-heading">
            <p className="eyebrow">Start lokalny</p>
            <h2>Przygotowanie środowiska</h2>
            <p>Podstawowe środowisko Python jest niezależne od instalacji COLMAP i Unreal Engine.</p>
          </div>
          <div>
            <pre><code>{commands}</code></pre>
            <div className="requirements">
              <div><strong>Python 3.11</strong><span>skrypty, PBR, geometria, walidacja</span></div>
              <div><strong>COLMAP</strong><span>rekonstrukcja fotogrametryczna</span></div>
              <div><strong>Blender</strong><span>ręczne korekty geometrii i blendshapes</span></div>
              <div><strong>Unreal Engine 5</strong><span>MetaHuman i finalny eksport</span></div>
            </div>
          </div>
        </section>

        <section className="section quality-section">
          <div className="section-heading"><p className="eyebrow">Kontrola jakości</p><h2>Kiedy awatar jest gotowy</h2></div>
          <div className="checklist">
            <span>Geometria zachowuje proporcje twarzy</span>
            <span>Rig i wszystkie wymagane blendshapes działają</span>
            <span>Brak clippingu przy skrajnych pozach</span>
            <span>Tekstury PBR reagują poprawnie na oświetlenie</span>
            <span>Animacje przechodzą płynnie bez skoków</span>
            <span>Lip sync jest zsynchronizowany z dźwiękiem</span>
            <span>Model został sprawdzony w docelowym silniku</span>
          </div>
        </section>
      </main>

      <footer>
        <div><strong>avatar-3d-self</strong><span>Realistyczny awatar 3D od zdjęć do silnika.</span></div>
        <div className="footer-links"><a href="#tools">Narzędzia</a><a href="https://github.com/MatPomGit/avatar-3d-self">Repozytorium</a></div>
      </footer>
    </div>
  )
}

export default App
