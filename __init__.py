import bpy, sys, os

from . TMG_Armature_Tools import *

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Thank you all that download, suggest, and request features
# As well as the whole Blender community. You're all epic :)


bl_info = {
    "name": "TMG_Armature_Tools",
    "author": "Johnathan Mueller",
    "descrtion": "A panel to manage atmosphere and lighting effects",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > TMG_Armature_Tools Tab",
    "warning": "",
    "category": "Object"
}

classes = (
    ## Properties
    TMG_Armature_Properties,

    ## Operators
    ARMATURE_OT_TMG_Clean_Mocap_Armature,
    ARMATURE_OT_TMG_Set_Bone_Euler,
    
    ## Material Panels
    ARMATURE_PT_TMG_Armature_Tools_Parent_Panel, 
    ARMATURE_PT_TMG_Armature_Tools_View_Panel,
    ARMATURE_PT_TMG_Armature_Tools_Panel, 
)

def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.tmg_armature_vars = bpy.props.PointerProperty(type=TMG_Armature_Properties)

def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)

if __name__ == "__main__":
    register()

