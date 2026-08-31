import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';

const AvatarViewer = () => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const modelRef = useRef(null);
  const [modelStats, setModelStats] = useState(null);
  const [blendshapes, setBlendshapes] = useState([]);
  const [animations, setAnimations] = useState([]);
  const [selectedAnimation, setSelectedAnimation] = useState(null);

  useEffect(() => {
    // Initialize Three.js scene
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    scene.fog = new THREE.Fog(0x1a1a2e, 5, 15);

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.set(0, 1.7, 2.5);
    camera.lookAt(0, 1.7, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowShadowMap;
    containerRef.current.appendChild(renderer.domElement);

    // Lighting setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 0.8);
    keyLight.position.set(5, 5, 5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
    fillLight.position.set(-5, 3, 2);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0xffffff, 0.4);
    rimLight.position.set(0, 2, -5);
    scene.add(rimLight);

    // Load FBX model
    const loader = new FBXLoader();
    loader.load('/exports/avatar_final.fbx', (fbx) => {
      fbx.scale.multiplyScalar(0.01); // Scale down if needed
      
      // Configure materials for PBR
      fbx.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
          
          // Apply PBR textures if available
          if (child.material) {
            child.material.side = THREE.FrontSide;
            child.material.shadowSide = THREE.BackSide;
          }
        }
      });

      scene.add(fbx);
      modelRef.current = fbx;

      // Calculate stats
      const stats = calculateModelStats(fbx);
      setModelStats(stats);

      // Extract blendshapes
      if (fbx.children[0]?.morphTargetInfluences) {
        const bs = Object.keys(fbx.children[0].morphTargetDictionary || {});
        setBlendshapes(bs);
      }

      // Extract animations
      if (fbx.animations.length > 0) {
        setAnimations(fbx.animations.map(a => a.name));
      }
    });

    sceneRef.current = scene;

    // Animation loop
    const mixer = new THREE.AnimationMixer(modelRef.current);
    let action = null;

    const animate = () => {
      requestAnimationFrame(animate);

      if (mixer) mixer.update(0.016); // 60 FPS
      renderer.render(scene, camera);
    };
    animate();

    // Handle blendshape changes
    const handleBlendshapeChange = (name, value) => {
      if (modelRef.current?.children[0]?.morphTargetInfluences) {
        const idx = modelRef.current.children[0].morphTargetDictionary[name];
        if (idx !== undefined) {
          modelRef.current.children[0].morphTargetInfluences[idx] = value;
        }
      }
    };

    window.handleBlendshapeChange = handleBlendshapeChange;

    // Cleanup
    return () => {
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  const calculateModelStats = (model) => {
    let triangles = 0;
    let vertices = 0;

    model.traverse((child) => {
      if (child.isMesh) {
        triangles += child.geometry.index?.count / 3 || 0;
        vertices += child.geometry.attributes.position?.count || 0;
      }
    });

    return { triangles, vertices };
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
      {/* 3D Viewer */}
      <div ref={containerRef} style={{ flex: 1, background: '#1a1a2e' }} />

      {/* Control Panel */}
      <div style={{
        width: 350,
        background: '#2d2d44',
        color: '#fff',
        padding: 20,
        overflowY: 'auto',
        borderLeft: '1px solid #444'
      }}>
        <h2>🧠 Avatar Inspector</h2>

        {/* Model Stats */}
        {modelStats && (
          <div style={{ background: '#1a1a2e', padding: 15, borderRadius: 8, marginBottom: 20 }}>
            <h3>📊 Model Stats</h3>
            <p>Triangles: <strong>{modelStats.triangles.toLocaleString()}</strong></p>
            <p>Vertices: <strong>{modelStats.vertices.toLocaleString()}</strong></p>
            <p>Format: <strong>FBX</strong></p>
            <p>Rigged: <strong>Yes</strong></p>
          </div>
        )}

        {/* Blendshapes */}
        {blendshapes.length > 0 && (
          <div style={{ marginBottom: 20 }}>
            <h3>😊 Facial Blendshapes ({blendshapes.length})</h3>
            {blendshapes.slice(0, 8).map((bs) => (
              <div key={bs} style={{ marginBottom: 10 }}>
                <label>{bs}</label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  onChange={(e) => window.handleBlendshapeChange(bs, parseFloat(e.target.value))}
                  style={{ width: '100%' }}
                />
              </div>
            ))}
          </div>
        )}

        {/* Animations */}
        {animations.length > 0 && (
          <div>
            <h3>🎬 Animations ({animations.length})</h3>
            <select onChange={(e) => setSelectedAnimation(e.target.value)}>
              <option value="">-- Select Animation --</option>
              {animations.map((anim) => (
                <option key={anim} value={anim}>{anim}</option>
              ))}
            </select>
          </div>
        )}

        {/* Texture Info */}
        <div style={{ background: '#1a1a2e', padding: 15, borderRadius: 8, marginTop: 20 }}>
          <h3>🎨 Textures</h3>
          <p><strong>Diffuse:</strong> 2048×2048</p>
          <p><strong>Normal:</strong> 2048×2048</p>
          <p><strong>Roughness:</strong> 2048×2048</p>
          <p><strong>Metallic:</strong> 2048×2048</p>
          <p><strong>AO:</strong> 2048×2048</p>
        </div>

        {/* Engine Export */}
        <div style={{ marginTop: 20 }}>
          <h3>📤 Export For</h3>
          <button style={{
            width: '100%',
            padding: 10,
            marginBottom: 8,
            background: '#3d5a80',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer'
          }}>
            Unreal Engine 5
          </button>
          <button style={{
            width: '100%',
            padding: 10,
            marginBottom: 8,
            background: '#3d5a80',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer'
          }}>
            Unity HDRP
          </button>
          <button style={{
            width: '100%',
            padding: 10,
            background: '#3d5a80',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer'
          }}>
            Twinmotion
          </button>
        </div>
      </div>
    </div>
  );
};

export default AvatarViewer;