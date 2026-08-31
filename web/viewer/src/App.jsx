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
    scene.background = new THREE.Color(0x0f172a)

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 420, 0.1, 1000)
    camera.position.set(0, 1.55, 2.7)
    camera.lookAt(0, 1.45, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(container.clientWidth, 420)
    container.appendChild(renderer.domElement)

    scene.add(new THREE.HemisphereLight(0xffffff, 0x334155, 2.2))
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
      <div className="section-heading">
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
        <a className="brand" href="#start">avatar-3d-self</a>
        <nav>
          <a href="#about">Projekt</a>
          <a href="#pipeline">Pipeline</a>
          <a href="#viewer">3D</a>
          <a href="#setup">Uruchomienie</a>
          <a href="https://github.com/MatPomGit/avatar-3d-self">GitHub</a>
        </nav>
      </header>

      <main>
        <section id="start" className="hero">
          <div className="hero-copy">
            <p className="eyebrow">Photogrammetry · MetaHuman · PBR · Animation</p>
            <h1>Realistyczny cyfrowy awatar 3D z pełnym pipeline’em produkcyjnym</h1>
            <p className="lead">Projekt łączy rekonstrukcję fotogrametryczną, przetwarzanie geometrii i tekstur, MetaHuman, blendshapes, animację, lip sync oraz eksport do silników 3D. Ta strona jest jednocześnie opisem projektu i instrukcją jego odtworzenia.</p>
            <div className="actions">
              <a className="button primary" href="#pipeline">Zobacz cały proces</a>
              <a className="button" href="#setup">Przygotuj środowisko</a>
            </div>
          </div>
          <div className="hero-panel">
            <span>Wejście</span><strong>Zdjęcia wielowidokowe</strong>
            <span>Rekonstrukcja</span><strong>COLMAP + mesh</strong>
            <span>Awatar</span><strong>MetaHuman + blendshapes</strong>
            <span>Wygląd</span><strong>PBR + materiały</strong>
            <span>Ruch</span><strong>Animacja + lip sync</strong>
            <span>Wyjście</span><strong>FBX / Unreal / Unity</strong>
          </div>
        </section>

        <section id="about" className="section split">
          <div className="section-heading">
            <p className="eyebrow">Cel</p>
            <h2>Jeden repozytoryjny przepływ od zdjęć do awatara</h2>
          </div>
          <div className="prose">
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
            {steps.map(([title, text]) => (
              <article className="step" key={title}>
                <h3>{title}</h3>
                <p>{text}</p>
              </article>
            ))}
          </div>
        </section>

        <Viewer />

        <section id="setup" className="section split">
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

        <section className="section">
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
        <strong>avatar-3d-self</strong>
        <span>Dokumentacja i interaktywny viewer publikowane automatycznie przez GitHub Pages.</span>
      </footer>
    </div>
  )
}

export default App
