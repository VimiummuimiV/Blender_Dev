bl_info = {
    "name": "Custom Hotkeys Manager",
    "author": "Patcher",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "3D View",
    "description": "Custom hotkey mappings with context-aware behavior",
    "category": "Interface",
}

import bpy


# ============================================================================
# OPERATORS
# ============================================================================

class MESH_OT_smart_knife_connect(bpy.types.Operator):
    """Smart Knife/Connect tool - Uses Knife when nothing selected, Connect when vertices selected"""
    bl_idname = "mesh.smart_knife_connect"
    bl_label = "Smart Knife/Connect"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        
        try:
            import bmesh
            bm = bmesh.from_edit_mesh(mesh)
            
            # Count selected vertices
            selected_verts = [v for v in bm.verts if v.select]
            
            if len(selected_verts) >= 2:
                # Multiple vertices selected - use connect
                bpy.ops.mesh.vert_connect()
                self.report({'INFO'}, "Connected vertices")
            else:
                # No or single vertex selected - use knife tool
                bpy.ops.mesh.knife_tool('INVOKE_DEFAULT')
                self.report({'INFO'}, "Knife tool activated")
                
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


# ============================================================================
# KEYMAP REGISTRATION
# ============================================================================

addon_keymaps = []

def register_keymaps():
    """Register custom keymaps"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if not kc:
        return
    
    # Create keymap for Mesh editing
    km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
    
    # Tilde (~) - Smart Knife/Connect
    kmi = km.keymap_items.new(
        MESH_OT_smart_knife_connect.bl_idname,
        type='ACCENT_GRAVE',  # Tilde/Grave accent key
        value='PRESS'
    )
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    """Unregister custom keymaps"""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


# ============================================================================
# REGISTRATION
# ============================================================================

classes = (
    MESH_OT_smart_knife_connect,
)


def register():
    """Register addon"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    register_keymaps()
    
    print("Custom Hotkeys addon registered")


def unregister():
    """Unregister addon"""
    unregister_keymaps()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("Custom Hotkeys addon unregistered")


if __name__ == "__main__":
    register()