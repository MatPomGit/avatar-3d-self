# Complete Avatar Production Pipeline

## Multi-Engine Universal Avatar

### Supported Engines
- ✅ Unreal Engine 5
- ✅ Unity (HDRP + URP)
- ✅ Twinmotion
- ✅ MetaHuman Creator
- ✅ Custom WebGL (THREE.js)

---

## Phase 1: PBR Texture Generation

### Input
- High-quality diffuse scan texture (4K+ recommended)

### Processing
```bash
python scripts/pbr_texture_processor.py \
  --diffuse references/photos/scan_2048.png \
  --output assets/textures/pbr
```

### Output
- diffuse.png (original scan)
- normal.png (surface detail)
- roughness.png (matte/glossy)
- metallic.png (non-metallic for skin)
- ao.png (ambient occlusion)

### Quality
- All textures: 2048×2048 (scalable to 4K)

## Phase 2: Multi-Engine Material Export

```bash
python scripts/material_converter.py
```

Generates material configs for:
- Unreal: M_Avatar_Master instance
- Unity: Standard/HDRP shader setup
- Twinmotion: PBR material definition

Each engine gets optimal settings (SSS for UE, properties for Unity, etc.)

## Phase 3: Lip Sync + Speech animation

Install Piper TTS
```bash
pip install piper-tts
piper --download-model en_US-libritts-high
```

Generate Lip Sync
```bash
python scripts/piper_lipsync_generator.py \
  --text "Hello world! My name is [Your Name]." \
  --output exports/speech
```

Output
- speech.wav - Synthesized audio
- phonemes.txt - Phoneme timeline
- lipsync_blendshapes.json - Blendshape keyframes (30 FPS)
- lipsync_fbx_format.json - Import-ready for game engines


## Phase 4: Web Viewer

### Build
```bash
cd web/viewer
npm install
npm run dev
```

### Access
- http://localhost:5173

### Features
✅ Real-time FBX preview
✅ Blendshape sliders
✅ Animation playback
✅ Model stats (triangles, vertices)
✅ Texture inspection
✅ Engine export buttons


## Phase 5: Cross-Engine Export

### Unreal Engine 5
- Import exports/avatar_final.fbx
- Apply material from exports/materials/- Skin_Face_UE5.json
- Assign lip sync to AnimBP_Speech
- Test in PIE

### Unity (HDRP)
- Import FBX → Assets/Characters/
- Create material from Skin_Face_Unity.json
- Assign to mesh
- Attach LipSyncController.cs script
- Play speech animation

### Twinmotion
- Import to Twinmotion
- Apply Skin_Face_Twinmotion.json material
- Use for architectural visualization

## Lip Sync Integration

### Phoneme-to-Blendshape Mapping
Vowels (a, e, i, o, u) → mouthOpen, mouthWide
Consonants (p, b, m) → lip press
Fricatives (f, v, s) → mouth position
Stops (t, d) → jaw open

### Real-Time Speech
```bash
# Import in your app
from piper_lipsync_generator import generate_speech_with_lipsync

text = "Welcome to my digital avatar"
generate_speech_with_lipsync(text, "exports/speech")
```



## Quality Checklist
[ ] PBR textures processed (5 maps)
[ ] Material configs for all engines
[ ] Web viewer renders correctly
[ ] All 48 blendshapes functional
[ ] Lip sync synced to audio
[ ] Model < 200k triangles (game-ready)
[ ] Animations smooth (no popping)
[ ] Tested in at least one engine

## Specs
Aspect
Spec
Geometry
~80-120k triangles (game-ready)
Textures
2048×2048 PBR (5 maps)
Blendshapes
48+ FACS-based
Animations
10+ locomotion/gesture
Lip Sync
Phoneme-driven, 30 FPS
Format
FBX universal


## GitHub Actions Automation
Pipeline runs on every push:
- Generate PBR textures
- Convert materials
- Create lip sync
- Build web viewer
- Validate all exports
- Create GitHub Release

### Check Actions tab for logs.
```bash
---

## 8. Dodaj to do `pyproject.toml`

```toml
[project.optional-dependencies]
pbr = ["pillow>=10.0", "numpy>=1.24", "scipy>=1.11"]
lipsync = ["piper-tts>=1.2"]
web = ["flask>=3.0", "flask-cors>=4.0"]
```


## PODSUMOWANIE: Copy-Paste Lista
- scripts/pbr_texture_processor.py ← PBR generacja
- scripts/material_converter.py ← Multi-engine konwersja
- scripts/piper_lipsync_generator.py ← Lip sync + TTS
- web/viewer/src/App.jsx ← THREE.js viewer
- .github/workflows/avatar_complete_pipeline.yml ← Automation
- docs/COMPLETE_PIPELINE.md ← Dokumentacja

Uruchom:
```bash
pip install pillow numpy scipy piper-tts
python scripts/pbr_texture_processor.py --diffuse scan.png --output assets/textures
python scripts/piper_lipsync_generator.py --text "Hello!" --output exports/speech
cd web/viewer && npm install && npm run dev
```

Model będzie dostępny na http://localhost:5173 z możliwością eksportu do wszystkich silników.

