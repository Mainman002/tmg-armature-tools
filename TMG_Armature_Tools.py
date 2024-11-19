from asyncio.windows_events import NULL
import bpy, sys, os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


def clean_mocap_armature():
    keywords = [ 'floor', 'ik_', '_ik', '_end', 'rootnode_0_' ]

    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            keywords.append( ob.name.lower().replace('liam_', '').replace('.001', '').replace('.002', '').replace('.003', '').replace('.004', '').replace('.005', '').replace('.006', '').replace('.007', '').replace('.008', '') )
            for weight in ob.vertex_groups:
                weight.name = weight.name.replace(':', '_')
                weight.name = weight.name.lower()

    for ob in bpy.context.selected_objects:
        if ob.type == "ARMATURE":
            ob.select_set(state=True)
            bpy.ops.object.editmode_toggle()
            if ob.mode == 'EDIT':
                bpy.ops.armature.select_all(action='DESELECT')
                for key in keywords:
                    for bone in ob.data.edit_bones:
                        bone.name = bone.name.lower()
                        bone.name = bone.name.replace(':', '_')
                        if key in bone.name:
                            ob.data.edit_bones.remove(bone)
                for bone in ob.data.edit_bones:
                    if bone.name == 'rl_boneroot':
                        bone.name = 'root'
            bpy.ops.object.editmode_toggle()
    return {'FINISHED'}


def set_bone_euler():
    for ob in bpy.context.selected_objects:
        if ob.type == "ARMATURE":
            ob.select_set(state=True)
            if ob.mode != 'POSE':
                bpy.ops.object.posemode_toggle()
                if ob.mode == 'POSE':
                    for bone in ob.pose.bones:
                        bone.rotation_mode = 'XYZ'
                bpy.ops.object.posemode_toggle()


def set_bone_infront(self, context):
    scene = context.scene
    tmg_armature_vars = scene.tmg_armature_vars

    for ob in bpy.context.scene.objects:
        if ob.type == 'ARMATURE':
            ob.show_in_front = tmg_armature_vars.in_front


class TMG_Armature_Properties(bpy.types.PropertyGroup):
    in_front : bpy.props.BoolProperty(name='In Front', default=False, update=set_bone_infront)


class ARMATURE_OT_TMG_Clean_Mocap_Armature(bpy.types.Operator):
    bl_idname = 'wm.armature_ot_tmg_clean_mocap_armature'
    bl_label = 'Mocap Armature'
    bl_description = 'Removes IK and floor bones, then renames bones and vertex weight groups'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        clean_mocap_armature()
        return {'FINISHED'}


class ARMATURE_OT_TMG_Set_Bone_Euler(bpy.types.Operator):
    bl_idname = 'wm.armature_ot_tmg_set_bone_euler'
    bl_label = 'Euler Rotation'
    bl_description = 'Sets pose bones to rotate in Euler XYZ mode'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        set_bone_euler()
        return {'FINISHED'}


class ARMATURE_PT_TMG_Armature_Tools_Parent_Panel(bpy.types.Panel):
    bl_idname = 'ARMATURE_PT_tmg_armature_parent_panel'
    bl_category = 'TMG'
    bl_label = 'Armature Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout


class ARMATURE_PT_TMG_Armature_Tools_View_Panel(bpy.types.Panel):
    bl_idname = 'ARMATURE_PT_tmg_armature_view_panel'
    bl_label = 'Viewport'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ARMATURE_PT_tmg_armature_parent_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        tmg_armature_vars = scene.tmg_armature_vars

        layout = self.layout    
        box = layout.box()
        col = box.column(align=True)

        col.prop(tmg_armature_vars, 'in_front')


class ARMATURE_PT_TMG_Armature_Tools_Panel(bpy.types.Panel):
    bl_idname = 'ARMATURE_PT_tmg_armature_panel'
    bl_label = 'Clean'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ARMATURE_PT_tmg_armature_parent_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        tmg_armature_vars = scene.tmg_armature_vars

        layout = self.layout    
        box = layout.box()
        col = box.column(align=True)

        objs = []
        for ob in bpy.context.selected_objects:
            if ob.mode == "OBJECT" and ob.type == 'ARMATURE':
                objs.append(ob)

        if len(objs) > 0:
            col.operator('wm.armature_ot_tmg_clean_mocap_armature')
            col.operator('wm.armature_ot_tmg_set_bone_euler')
        
        if not len(objs) > 0:
            col.label(text='Please Select Armature')

        # layout.operator("tmg_atmosphere.add", icon='SCENE_DATA')
        # layout.operator("tmg_atmosphere.set_scene_settings", icon='SCENE')
