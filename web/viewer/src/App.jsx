import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'

const tabs = [
  ['start', 'Start'], ['pipeline', 'Pipeline'], ['pbr', 'Tekstury PBR'], ['uv', 'Mapy UV'],
  ['blendshapes', 'Blendshapes'], ['tools', 'Narzędzia'], ['viewer', 'Model 3D'],
  ['setup', 'Uruchomienie'], ['quality', 'Kontrola jakości'],
]

const steps = [
  ['Przygotowanie zdjęć', 'Zrób serię ostrych zdjęć twarzy z wielu kierunków.'],
  ['Rekonstrukcja 3D', 'Zbuduj geometrię ze zdjęć za pomocą COLMAP.'],
  ['MetaHuman i geometria twarzy', 'Dopasuj model bazowy do zeskanowanej twarzy.'],
  ['Blendshapes i korekty', 'Przygotuj kształty twarzy potrzebne do mimiki.'],
  ['Tekstury PBR', 'Przygotuj kolor, normal, roughness, metallic i AO.'],
  ['Animacja i lip sync', 'Dodaj ruch twarzy, ciała i synchronizację ust z głosem.'],
  ['Eksport', 'Wyeksportuj gotowy model do FBX.'],
  ['Walidacja', 'Sprawdź geometrię, materiały, mimikę i animacje w silniku docelowym.'],
]

const tools = [
  ['Python 3.11', 'Środowisko skryptów projektu.', 'wymagane', 'https://www.python.org/downloads/release/python-31116/'],
  ['COLMAP', 'Tworzy model 3D ze zdjęć.', 'dla skanu', 'https://colmap.github.io/install.html'],
  ['Blender', 'Edycja geometrii, UV i blendshapes.', 'zalecane', 'https://www.blender.org/download/'],
  ['Unreal Engine 5', 'MetaHuman, materiały i test modelu.', 'dla MetaHuman', 'https://www.unrealengine.com/download'],
  ['MetaHuman', 'Rig i animacja cyfrowej postaci.', 'UE5', 'https://www.metahuman.com/create'],
  ['Piper TTS', 'Opcjonalny syntezator mowy do lip sync.', 'opcjonalne', 'https://github.com/OHF-Voice/piper1-gpl'],
]

const pbrMaps = [
  ['Base Color / Albedo', 'Kolor powierzchni bez cieni i połysku.', 'RGB, sRGB'],
  ['Normal', 'Udaje drobne nierówności bez dodawania geometrii.', 'RGB, liniowa'],
  ['Roughness', 'Czerń jest gładka, biel matowa.', 'skala szarości'],
  ['Smoothness', 'Odwrotność roughness. Im jaśniej, tym gładsza powierzchnia.', 'skala szarości'],
  ['Metallic', 'Mówi, które miejsca zachowują się jak metal.', 'skala szarości'],
  ['Ambient Occlusion', 'Przyciemnia szczeliny i trudno dostępne miejsca.', 'skala szarości'],
  ['Height / Displacement', 'Opisuje wysokość i większe nierówności powierzchni.', 'skala szarości'],
  ['Emissive', 'Wskazuje miejsca, które mają świecić.', 'RGB'],
  ['Opacity / Alpha', 'Steruje przezroczystością lub wycięciami.', 'alpha / szarość'],
]

const engineRows = [
  ['Kolor', 'Base Map', 'Base Color', 'Color'],
  ['Gładkość', 'Smoothness', 'Roughness', 'Roughness'],
  ['Metal', 'Metallic', 'Metallic', 'Metallic'],
  ['Normal', 'Normal Map', 'Normal', 'Normal'],
  ['AO', 'Occlusion Map', 'Ambient Occlusion', 'zależnie od materiału'],
  ['Emisja', 'Emission', 'Emissive Color', 'Emissive'],
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
    const scene = new THREE.Scene(); scene.background = new THREE.Color(0x08111f)
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 440, 0.1, 1000)
    camera.position.set(0, 1.55, 2.7); camera.lookAt(0, 1.45, 0)
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); renderer.setSize(container.clientWidth, 440)
    container.appendChild(renderer.domElement)
    scene.add(new THREE.HemisphereLight(0xffffff, 0x22324b, 2.2))
    const key = new THREE.DirectionalLight(0xffffff, 2.5); key.position.set(3, 4, 3); scene.add(key)
    let model = null; let frameId = 0
    new FBXLoader().load(`${import.meta.env.BASE_URL}model/avatar_final.fbx`, (fbx) => {
      model = fbx; fbx.scale.multiplyScalar(0.01)
      let triangles = 0; let vertices = 0
      fbx.traverse((child) => { if (child.isMesh) { const count = child.geometry.attributes.position?.count || 0; vertices += count; triangles += child.geometry.index ? child.geometry.index.count / 3 : count / 3 } })
      setStats({ triangles: Math.round(triangles), vertices }); setStatus('Model gotowy'); scene.add(fbx)
    }, undefined, () => setStatus('Model FBX nie został jeszcze opublikowany.'))
    const animate = () => { frameId = requestAnimationFrame(animate); if (model) model.rotation.y += 0.0025; renderer.render(scene, camera) }
    animate()
    const resize = () => { const width = container.clientWidth; camera.aspect = width / 440; camera.updateProjectionMatrix(); renderer.setSize(width, 440) }
    window.addEventListener('resize', resize)
    return () => { cancelAnimationFrame(frameId); window.removeEventListener('resize', resize); renderer.dispose(); renderer.domElement.remove() }
  }, [])
  return <div className="viewer-card"><div ref={containerRef} className="viewer-canvas" /><div className="viewer-meta"><strong>{status}</strong>{stats && <span>{stats.triangles.toLocaleString()} trójkątów · {stats.vertices.toLocaleString()} wierzchołków</span>}</div></div>
}

function App() {
  const initialTab = tabs.some(([id]) => id === window.location.hash.slice(1)) ? window.location.hash.slice(1) : 'start'
  const [activeTab, setActiveTab] = useState(initialTab)
  useEffect(() => { const f = () => { const id = window.location.hash.slice(1); if (tabs.some(([x]) => x === id)) setActiveTab(id) }; window.addEventListener('hashchange', f); return () => window.removeEventListener('hashchange', f) }, [])
  const openTab = (id) => { setActiveTab(id); window.history.replaceState(null, '', `#${id}`); window.scrollTo({ top: 0, behavior: 'smooth' }) }

  return <div className="app-shell">
    <header className="topbar"><button className="brand brand-button" onClick={() => openTab('start')}><span className="brand-mark">A3</span><span>avatar-3d-self</span></button><nav className="desktop-nav" aria-label="Główna nawigacja">{tabs.map(([id,label]) => <button key={id} className={activeTab === id ? 'nav-tab active' : 'nav-tab'} onClick={() => openTab(id)}>{label}</button>)}<a className="nav-github" href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">GitHub ↗</a></nav></header>
    <div className="mobile-tabs">{tabs.map(([id,label]) => <button key={id} className={activeTab === id ? 'mobile-tab active' : 'mobile-tab'} onClick={() => openTab(id)}>{label}</button>)}</div>

    <main className="tab-main">
      {activeTab === 'start' && <section className="tab-view home-view"><div className="home-copy"><div className="hero-badge">Projekt otwartoźródłowy</div><p className="eyebrow">Fotogrametria · MetaHuman · PBR · Animacja</p><h1>Realistyczny cyfrowy awatar 3D</h1><p className="lead">Od zdjęć człowieka do gotowej, animowanej postaci 3D.</p><div className="actions"><button className="button primary" onClick={() => openTab('pipeline')}>Zobacz pipeline</button><button className="button" onClick={() => openTab('uv')}>Jak działa UV?</button></div></div><div className="home-dashboard"><div className="metric"><strong>8</strong><span>etapów</span></div><div className="metric"><strong>FBX</strong><span>format modelu</span></div><div className="metric"><strong>UE5</strong><span>silnik docelowy</span></div><div className="flow-card"><span>Zdjęcia</span><b>→</b><span>Model 3D</span><b>→</b><span>UV</span><b>→</b><span>PBR</span><b>→</b><span>Animacja</span></div></div></section>}

      {activeTab === 'pipeline' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Procedura</p><h2>Pipeline produkcyjny</h2><p>Osiem kroków od zdjęć do gotowej postaci.</p></div><div className="steps">{steps.map(([title,text],i) => <article className="step" key={title}><span className="step-number">{String(i+1).padStart(2,'0')}</span><h3>{title}</h3><p>{text}</p></article>)}</div></section>}

      {activeTab === 'pbr' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Materiały</p><h2>Tekstury PBR</h2><p>Każda mapa opisuje inną cechę powierzchni modelu.</p></div><div className="pbr-grid">{pbrMaps.map(([name,role,format]) => <article className="pbr-card" key={name}><div><h3>{name}</h3><span className="pbr-format">{format}</span></div><p>{role}</p></article>)}</div><div className="comparison-block"><div className="section-subheading"><h3>Unity, Unreal Engine i Twinmotion</h3><p>Te same dane mogą mieć inne nazwy.</p></div><div className="comparison-table-wrap"><table className="comparison-table"><thead><tr><th>Cecha</th><th>Unity</th><th>Unreal Engine</th><th>Twinmotion</th></tr></thead><tbody>{engineRows.map(row => <tr key={row[0]}>{row.map((cell,i) => i === 0 ? <th key={cell}>{cell}</th> : <td key={cell}>{cell}</td>)}</tr>)}</tbody></table></div></div><div className="pbr-notes"><article><strong>Najważniejsze</strong><p>Unreal i Twinmotion używają roughness. Unity często używa smoothness. To wartości odwrotne: smoothness = 1 − roughness.</p></article><article><strong>Normal map</strong><p>Jeśli wypukłości wyglądają jak wklęsłości, zwykle trzeba odwrócić zielony kanał mapy normalnej.</p></article></div></section>}

      {activeTab === 'uv' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Teksturowanie</p><h2>Mapy UV postaci</h2><p>UV mówi komputerowi, który fragment obrazka ma trafić na konkretny fragment modelu 3D.</p></div><div className="pbr-notes"><article><strong>Najprościej</strong><p>Wyobraź sobie papierową maskę twarzy. Rozcinasz ją i rozkładasz płasko na stole. Model 3D to maska, a jej płaskie kawałki to mapa UV.</p></article><article><strong>U i V</strong><p>To po prostu dwie osie na płaskim obrazku. U oznacza kierunek poziomy, V pionowy. Każdy wierzchołek modelu dostaje współrzędne UV.</p></article><article><strong>Po co to jest?</strong><p>Dzięki UV silnik wie, gdzie na głowie narysować oczy, usta, skórę, pieprzyk albo fragment ubrania. Bez poprawnego UV tekstura będzie przesunięta, rozciągnięta albo pomieszana.</p></article><article><strong>Wyspy UV</strong><p>Model rozcina się na płaskie kawałki zwane wyspami UV. Twarz, uszy, szyja czy tułów mogą być osobnymi wyspami.</p></article><article><strong>Szwy</strong><p>Szew to miejsce, w którym model został „rozcięty” na potrzeby UV. Najlepiej umieszczać szwy tam, gdzie są mało widoczne, np. z tyłu głowy.</p></article><article><strong>Rozciąganie</strong><p>Jeżeli wyspa UV ma zły kształt, tekstura się rozciąga. Okrągły pieprzyk może wtedy wyglądać jak długa plama. To znak, że UV trzeba poprawić.</p></article></div><div className="info-strip"><strong>Zapamiętaj:</strong><span>UV nie zmienia kształtu modelu. UV mówi tylko, jak przykleić płaski obraz 2D do powierzchni 3D.</span></div></section>}

      {activeTab === 'blendshapes' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Mimika twarzy</p><h2>Blendshapes</h2><p>Blendshape to zapamiętany wariant kształtu tej samej twarzy, np. uśmiech, mrugnięcie albo otwarte usta.</p></div><div className="pbr-notes"><article><strong>Jak to działa?</strong><p>Mamy twarz neutralną. Kopiujemy ją i przesuwamy część wierzchołków, np. unosimy kąciki ust. Program zapamiętuje różnicę między twarzą neutralną a uśmiechem.</p></article><article><strong>Waga</strong><p>Blendshape ma wartość określającą jego siłę. 0 oznacza brak efektu. Pełna wartość oznacza cały zapisany ruch. W Unity typowy zakres w interfejsie to 0–100.</p></article><article><strong>Można je mieszać</strong><p>Nie trzeba wybierać jednej miny. Można jednocześnie lekko się uśmiechać, mrużyć oczy i unosić brew. Końcowa twarz jest mieszanką kilku blendshapes.</p></article><article><strong>Przykłady</strong><p>Mrugnięcie lewego oka, mrugnięcie prawego oka, uśmiech, zmarszczenie brwi, uniesienie brwi, otwarcie szczęki, wysunięcie ust i ruch kącików ust.</p></article><article><strong>Mówienie</strong><p>Blendshapes mogą ustawiać usta w kształty potrzebne do mowy. System lip sync zmienia ich wagi w czasie, dzięki czemu usta poruszają się zgodnie z dźwiękiem.</p></article><article><strong>Blendshape a kość</strong><p>Kość obraca lub przesuwa fragment modelu. Blendshape zmienia położenie konkretnych wierzchołków. Mimika zwykle korzysta z obu metod jednocześnie.</p></article></div><div className="info-strip"><strong>Zapamiętaj:</strong><span>Blendshape nie jest osobnym modelem twarzy. To zapis informacji, jak wierzchołki jednej siatki mają się przesunąć.</span></div></section>}

      {activeTab === 'tools' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Narzędzia</p><h2>Środowisko pracy</h2><p>Instaluj tylko to, czego potrzebujesz na danym etapie.</p></div><div className="tool-grid">{tools.map(([name,role,tag,href]) => <a className="tool-card" href={href} key={name} target="_blank" rel="noreferrer"><div className="tool-card-top"><strong>{name}</strong><span className="tool-tag">{tag}</span></div><p>{role}</p><span className="tool-link">Oficjalna strona <b>↗</b></span></a>)}</div></section>}
      {activeTab === 'viewer' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Podgląd</p><h2>Interaktywny model 3D</h2><p>Tutaj pojawi się finalny model FBX.</p></div><Viewer /></section>}
      {activeTab === 'setup' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Start lokalny</p><h2>Uruchomienie repozytorium</h2></div><div className="setup-grid"><pre><code>{commands}</code></pre><div className="requirements"><div><strong>Python 3.11</strong><span>skrypty</span></div><div><strong>COLMAP</strong><span>rekonstrukcja</span></div><div><strong>Blender</strong><span>geometria i UV</span></div><div><strong>Unreal Engine 5</strong><span>MetaHuman i eksport</span></div></div></div></section>}
      {activeTab === 'quality' && <section className="tab-view"><div className="page-heading"><p className="eyebrow">Kontrola jakości</p><h2>Kiedy model jest gotowy?</h2></div><div className="checklist"><span>Twarz ma poprawne proporcje</span><span>UV nie rozciąga tekstur</span><span>Materiały PBR wyglądają poprawnie</span><span>Blendshapes nie psują twarzy</span><span>Rig i animacje działają</span><span>Lip sync pasuje do głosu</span><span>Model działa w docelowym silniku</span></div></section>}
    </main>
    <footer><div><strong>avatar-3d-self</strong><span>Od zdjęć do animowanej postaci 3D.</span></div><a href="https://github.com/MatPomGit/avatar-3d-self" target="_blank" rel="noreferrer">Repozytorium GitHub ↗</a></footer>
  </div>
}

export default App
