# Realistic & natural avatar creation guide

## Realism goals

Your avatar should achieve:
- **Geometric fidelity**: Realistic proportions from photogrammetry
- **Skin microdetails**: Normal maps, subsurface scattering
- **Natural animation**: Realistic eye gaze, breathing, micro-expressions
- **Lip-sync**: Audio-driven mouth movement
- **Unique features**: Facial asymmetries, individual characteristics

## Phase 1: High-Fidelity scanning

### Optimal photo capture

- Lighting: 3-point lighting (front key light, fill, back rim)
- Count: 100-150 photos from all angles
- Resolution: 4K minimum per photo
- Coverage: Front, 3/4s, profiles, top-down, angled up
- Expression: Neutral face + slight smile

### COLMAP settings for Face Precision

```bash
photogrammetry_pipeline.py --photos references/photos/raw 
--output source/scans/colmap_output 
--max-resolution 4096
```


## Phase 2: MetaHuman customization

1. **Visit**: https://www.metahuman.com/creator
2. **Customize**:
   - Head shape/size to match your scan
   - Skin tone, pore details
   - Hair style
   - Eye color
   - Mouth/teeth morphology
3. **Download**: FBX format with all blendshapes
4. **Save**: `source/metahuman/metahuman_base.fbx`

## Phase 3: 48+ Facial blendshapes

Run metadata generator:
```bash
python scripts/metahuman_processor.py
```

This creates blendshape_manifest.json with 48 realistic targets:
- 8 eye controls (blinks, looks)
- 12 brow controls (raises, furrows)
- 16 mouth controls (open, smile, corners)
- 6 jaw controls (open, shift, forward)
- 7 emotion meta-blends (happy, sad, angry, etc.)

### Manual sculpting (Blender)

For maximum realism, sculpt subtle details:
- Eye moisture/tears
- Under-eye bags (when relaxed)
- Cheek dimples (when smiling)
- Mouth corner tension
- Nostril flare

## Phase 4: Natural animations

### Body Animation Sources

- Mixamo (free mocap library): Walk, run, gestures, idles
- Custom capture: Record yourself with iPhone for personalization

### Critical animations for realism

- Breathing cycle (0.5s in/out) - always subtle
- Eye blinks (random 0.1-0.4s intervals, 3-5 per minute)
- Micro head movements (slight nods, looks while listening)
- Idle gestures (hand near face, weight shifts)
- Speech animation (lipsync + jaw movement)

### Bake Settings

```bash
python scripts/animation_baking.py
```
Export @ 30 FPS for locomotion, 60 FPS for facial.

## Phase 5: Rigging & Testing

Skeleton: MetaHuman comes pre-rigged
Blendshapes: All 48+ morphs integrated
Materials: PBR textures (diffuse, normal, roughness, metallic)

### Test in Engine:
- Import FBX to Unreal/Unity
- Play all blendshapes (sliders)
- Test animation blending
- Check clipping, deformation

### Quality checklist
[ ] Scanned geometry accurate to real face
[ ] All 48 blendshapes responsive
[ ] Blinks smooth & natural timing
[ ] Smile raises cheeks (not just mouth)
[ ] Animations loop without popping
[ ] No mesh clipping during extreme poses
[ ] Skin materials react to lighting
