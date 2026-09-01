# Complete Engine Integration Guide

## Unreal Engine 5

### Import Process
1. **File → Open** → Select `exports/unreal_engine_5/avatar_UE5.fbx`
2. **FBX Import Settings:**
   - ✓ Import Skeletal Mesh
   - ✓ Create Physics Asset: False
   - Material Search Location: Empty
   - Normal Import Method: Import Normals and Tangents

3. **Material Setup:**
   ```
   Content/Characters/
   ├── SKM_Avatar
   ├── M_Skin_Master (Material)
   ├── MI_Skin_Face (Material Instance)
   └── Textures/
       ├── T_Skin_Diffuse
       ├── T_Skin_Normal
       ├── T_Skin_Roughness
       └── T_Skin_AO
   ```

4. **Blueprint Setup:**
   - Create `BP_Avatar` actor
   - Add Skeletal Mesh Component
   - Assign `SKM_Avatar`
   - Add `AnimBP_Default` (IK + blendshapes)

### Blendshape Animation (Niagara/Sequencer)
```

Sequencer Panel:
├── Character
│   ├── eyeBlink_L (Morph Target Track)
│   ├── eyeBlink_R
│   ├── mouthOpen
│   ├── expression_Happy
│   └── ...48 total
```

---

## Unity HDRP

### Import Process
1. **Assets → Import New Asset** → Select FBX
2. **Model Settings:**
   - Rig: Humanoid
   - Animation Type: Humanoid
   - Import Materials: ✓

3. **Material Setup (HDRP):**
   - Shader: `HDRP/Lit`
   - Assign textures:
     - Base Map: Diffuse
     - Normal Map: Normal
     - Mask Map (Red=Metallic, Green=AO, Blue=Detail, Alpha=Smoothness)

4. **Script: LipSyncController.cs**
```csharp
using UnityEngine;

public class LipSyncController : MonoBehaviour {
    SkinnedMeshRenderer smr;
    
    void Start() {
        smr = GetComponent<SkinnedMeshRenderer>();
    }
    
    public void SetBlendshape(string name, float value) {
        var mesh = smr.sharedMesh;
        int index = mesh.GetBlendShapeIndex(name);
        if (index >= 0) {
            smr.SetBlendShapeWeight(index, value * 100);
        }
    }
}
```

---

## Twinmotion

### Import Process
1. **Content Manager** → Drag FBX
2. **Material Setup:**
   - Material Library → Create from JSON
   - Assign `Skin_Face_Twinmotion.json`
3. **Lighting:**
   - 3-point setup (Key, Fill, Rim)
   - Subsurface scattering enabled for skin

---

## Web (THREE.js)

```javascript
import * as THREE from 'three';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';

const loader = new FBXLoader();
const avatar = await loader.loadAsync('/exports/avatar_final.fbx');

// Apply textures
const textures = ['diffuse', 'normal', 'roughness', 'ao'];
avatar.traverse(child => {
  if (child.isMesh) {
    // Load PBR textures
    const map = new THREE.TextureLoader().load('assets/textures/pbr/diffuse.png');
    child.material.map = map;
  }
});

// Blendshape control
function setBlendshape(name, value) {
  avatar.children[0].morphTargetInfluences[
    avatar.children[0].morphTargetDictionary[name]
  ] = value;
}
```

---

## Lip Sync Integration (All Engines)

### Audio + Blendshape Sync
```json
{
  "speech": "Hello world",
  "keyframes": {
    "0": { "mouthOpen": 0.0 },
    "10": { "mouthOpen": 0.8, "mouthWide": 0.3 },
    "20": { "mouthOpen": 0.5, "mouthWide": 0.5 },
    "30": { "mouthOpen": 0.0 }
  }
}
```

### Implementation
- **Unreal:** Sequencer curves synchronized with audio
- **Unity:** Coroutine reading keyframe times
- **Web:** requestAnimationFrame loop

---

## Performance Targets

| Engine | Target FPS | Poly Budget | VRAM Budget |
|--------|-----------|-------------|------------|
| UE5 | 60 | 150k | 512 MB |
| Unity | 60 | 100k | 256 MB |
| Twinmotion | 30 | 200k | 1 GB |
| Web | 30-60 | 20k | 64 MB |

---

## Troubleshooting

### Materials not loading
- Check texture paths in material JSON
- Ensure textures copied to engine project

### Blendshapes not working
- Verify blendshape count > 0 in FBX
- Check morph target naming consistency

### Animation clipping
- Increase LOD distance for higher poly mesh
- Adjust bone weight limits per engine

---

See `ENGINE_INTEGRATION_CHECKLIST.md` for per-engine checklist.
```

---

## 8. GitHub Actions: Complete CI/CD

**`.github/workflows/complete_avatar_build.yml`**

```yaml
name: Complete Avatar Build & Validation

on:
  push:
    branches: [main]
    paths:
      - "scripts/**"
      - "source/**"
      - "references/**"
  workflow_dispatch:

jobs:
  validate_fbx:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Validate FBX
        run: |
          python scripts/fbx_validator.py exports/avatar_final.fbx \
            --html artifacts/fbx_validation.html
      
      - name: Analyze performance
        run: |
          python scripts/performance_analyzer.py \
            --triangles 80000 \
            --vertices 40000 \
            --bones 60 \
            --blendshapes 48 \
            --materials 3 \
            --platform pc_vr_high \
            --output artifacts/performance_pc.json
      
      - name: Upload validation report
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: artifacts/

  export_multi_engine:
    runs-on: ubuntu-latest
    needs: validate_fbx
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Create multi-engine exports
        run: |
          python scripts/export_manager.py \
            --base-fbx exports/avatar_final.fbx \
            --all \
            --output-dir exports
      
      - name: Upload engine exports
        uses: actions/upload-artifact@v3
        with:
          name: engine-exports
          path: exports/*/avatar_*.fbx

  build_web_viewer:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install & build viewer
        run: |
          cd web/viewer
          npm install
          npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web/viewer/dist

  create_release:
    runs-on: ubuntu-latest
    needs: [validate_fbx, export_multi_engine, build_web_viewer]
    if: success()
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: avatar-build-${{ github.run_number }}
          files: exports/**/avatar_*.fbx
          draft: false
```

---

## PODSUMOWANIE: Copy-Paste Lista

Skopiuj wszystkie te 8 programów:

1. **`scripts/fbx_validator.py`** ← Walidacja FBX + HTML report
2. **`scripts/mesh_optimizer.py`** ← Optymalizacja geometrii
3. **`scripts/uv_analyzer.py`** ← Analiza UV + poradnik
4. **`scripts/performance_analyzer.py`** ← Analiza wydajności dla każdej platformy
5. **`scripts/export_manager.py`** ← Multi-engine eksport
6. **`web/backend/app.py`** ← Flask REST API
7. **`docs/ENGINE_INTEGRATION.md`** ← Pełny poradnik integracji
8. **`.github/workflows/complete_avatar_build.yml`** ← Full CI/CD pipeline

**Uruchom lokalnie:**
```bash
# Validacja
python scripts/fbx_validator.py exports/avatar_final.fbx

# Performance
python scripts/performance_analyzer.py --triangles 80000 --platform pc_vr_high

# Export dla wszystkich silników
python scripts/export_manager.py --base-fbx exports/avatar_final.fbx --all

# Backend API
cd web/backend && pip install flask flask-cors && python app.py
```

**Wynik:** Pełny pipeline production-ready z automatyczną walidacją, optymalizacją, multi-engine supportem i web viewerem.