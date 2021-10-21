# exports each selected object into its own file

bl_info = {
    "name": "FBX Export Helper",
    "author": "Simon, Blender",
    "version": (1, 0, 0),
    "blender": (2, 93, 5),
    "location": "3D Viewport N Panel",
    "description": "description hereh",
    "warning": "",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}


import bpy
import os


class VIEW3D_PT_ExpoPanel(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "Export in Batches"
    bl_idname = "VIEW3D_PT_expoPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Batch Exporter'
    
    def draw(self, context):
        self.layout.label(text = "Export selected meshes")
        self.layout.operator('myops.fbxbatchexport')    
    

class EXP_OT_fbxbatchexport(bpy.types.Operator):
    """Exports all selected objects in the scene as seperate FBX files in the original file path."""
    bl_idname = "myops.fbxbatchexport"
    bl_label = "FBX Batch Exporter"

    #def invoke(self, context, event):
     
    def execute(self, context):
        
        # export to blend file location
        basedir = os.path.dirname(bpy.data.filepath)

        if not basedir:
            raise Exception("Blend file is not saved")

        view_layer = bpy.context.view_layer

        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in selection:

            obj.select_set(True)

            # some exporters only use the active object
            view_layer.objects.active = obj

            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(basedir, name)

            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True)

            # Can be used for multiple formats
            # bpy.ops.export_scene.x3d(filepath=fn + ".x3d", use_selection=True)

            obj.select_set(False)

            print("written:", fn)

        view_layer.objects.active = obj_active

        for obj in selection:
            obj.select_set(True)
        
            return {'FINISHED'}    


def register():
    bpy.utils.register_class(EXP_OT_fbxbatchexport)
    bpy.utils.register_class(VIEW3D_PT_ExpoPanel)
    print("registered class")
    
def unregister():
     bpy.utils.unregister_class(EXP_OT_fbxbatchexport)
     bpy.utils.unregister_class(VIEW3D_PT_ExpoPanel)
     print("unregistered class")
     
#this function only calls to register the function when the code is actually run
#if __name__ == '__main__':
    #register()