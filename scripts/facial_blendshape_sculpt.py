#!/usr/bin/env python3
"""
Blender-based blendshape generation and sculpting automation.
Run inside Blender: blender -b avatar.blend -P facial_blendshape_sculpt.py
"""
import bpy
import bmesh
import json
from pathlib import Path

class BlendshapeSculptor:
    def __init__(self, base_mesh_name: str = "Face_Base"):
        self.base_mesh = bpy.data.objects.get(base_mesh_name)
        if not self.base_mesh:
            raise ValueError(f"Mesh '{base_mesh_name}' not found in blend file")
        
        self.blendshapes = []
    
    def create_shapekey(self, name: str, is_basis: bool = False) -> bpy.types.ShapeKey:
        """Create empty shapekey (basis or target)"""
        if not self.base_mesh.data.shape_keys:
            self.base_mesh.shape_key_add(name="Basis")
        
        sk = self.base_mesh.shape_key_add(name=name)
        if is_basis:
            self.base_mesh.data.shape_keys.key_blocks[name].value = 1.0
        
        return sk
    
    def sculpt_blendshape(self, shapekey_name: str, modifier_func) -> None:
        """
        Apply vertex deformation to shapekey.
        modifier_func: callable(bmesh, shapekey_verts) -> modifies geometry
        """
        sk = self.base_mesh.data.shape_keys.key_blocks[shapekey_name]
        
        # Switch to edit mode
        bpy.context.view_layer.objects.active = self.base_mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        bm = bmesh.from_edit_mesh(self.base_mesh.data)
        
        # Apply custom modifier
        modifier_func(bm, sk.data)
        
        bmesh.update_edit_mesh(self.base_mesh.data)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def create_blink_l(self) -> None:
        """Left eye blink blendshape"""
        sk = self.create_shapekey("eyeBlink_L")
        
        def sculpt(bm, sk_verts):
            # Close left eye (move lids together)
            for vert in bm.verts:
                co = vert.co
                # Target left eye region: X < -0.02, Y ≈ 0.08-0.12
                if -0.05 < co.x < -0.02 and 0.07 < co.y < 0.13:
                    if co.y > 0.10:  # Upper lid moves down
                        vert.co.z -= 0.003
                    else:  # Lower lid moves up
                        vert.co.z += 0.002
        
        self.sculpt_blendshape("eyeBlink_L", sculpt)
    
    def create_mouth_open(self) -> None:
        """Mouth open blendshape"""
        sk = self.create_shapekey("mouthOpen")
        
        def sculpt(bm, sk_verts):
            # Open jaw + mouth corners down
            for vert in bm.verts:
                co = vert.co
                # Mouth region: -0.01 < X < 0.01, Y < 0.06
                if -0.015 < co.x < 0.015 and co.y < 0.08:
                    if co.y > 0.03:  # Upper lip moves up
                        vert.co.z += 0.005
                    elif co.y > -0.02:  # Lower lip moves down
                        vert.co.z -= 0.008
        
        self.sculpt_blendshape("mouthOpen", sculpt)
    
    def create_smile(self) -> None:
        """Smile expression blendshape"""
        sk = self.create_shapekey("expression_Happy")
        
        def sculpt(bm, sk_verts):
            # Mouth corners up, cheeks up, eyes squint
            for vert in bm.verts:
                co = vert.co
                # Mouth corners
                if abs(co.x) > 0.018 and 0.00 < co.y < 0.06:
                    vert.co.z += 0.006  # Raise corners
                # Cheeks
                elif abs(co.x) > 0.025 and 0.08 < co.y < 0.12:
                    vert.co.y += 0.002  # Puff cheeks
        
        self.sculpt_blendshape("expression_Happy", sculpt)
    
    def batch_create_basic_blendshapes(self) -> None:
        """Generate foundation 10 blendshapes"""
        blendshapes = [
            ("eyeBlink_L", self.create_blink_l),
            ("mouthOpen", self.create_mouth_open),
            ("expression_Happy", self.create_smile),
        ]
        
        for name, creator_func in blendshapes:
            try:
                creator_func()
                print(f"✓ Created: {name}")
                self.blendshapes.append(name)
            except Exception as e:
                print(f"✗ Failed to create {name}: {e}")
    
    def export_blendshape_fbx(self, output_path: str) -> None:
        """Export mesh with all blendshapes to FBX"""
        bpy.ops.export_scene.fbx(
            filepath=output_path,
            use_selection=False,
            object_types={'MESH', 'ARMATURE'},
            use_mesh_modifiers=False,
            use_custom_props=True,
            axis_forward='-Y',
            axis_up='Z'
        )
        print(f"✓ Exported: {output_path}")

# Run inside Blender
if __name__ == "__main__":
    sculptor = BlendshapeSculptor()
    sculptor.batch_create_basic_blendshapes()
    sculptor.export_blendshape_fbx("exports/avatar_with_blendshapes.fbx")