###
# file: zerogmodule.py
#
# language: python3
# version: 4.
# date: 2017-05-06
# author: bue
# license: GPL>=3
#
# run:
#    from zerogravity.zerogmodule import Module
#
# description:
#    plug in module library for zerogravity.zerog
#
# requirements:
#    python > 3.6
###

import importlib
import json
import sys
from typing import Dict, List, Optional, Set, Tuple

# constant
d_CODE = {
    "es_import": None,
    "ls_code" : None,
}

# error handling
with open(
        "{}/error.json".format(
            importlib.util.find_spec(
                "zerogravity"
            ).submodule_search_locations[0]
        )) as f_json:
    ds_error = json.load(f_json)


# plugin classes
class Code():
    def __init__(self, d_code: Dict) -> None:
        """
        input:
            d_code: dictionary of blender python code, structures in
            d_code['es_import']: import part of the code packed as string set
            d_code['ls_code']: main part of the code packed as string list

        output:
            Code.d_code: code object

        description:
            generic zerog code object
        """
        print("{}".format(ds_error["code_initialize"]))
        if not (set(d_CODE.keys()).intersection(set(d_code.keys()))):
            sys.exit("Error at zerogmodule.py Code.__init__: {}".format(
                ds_error["code_dict"].format(set(d_CODE.keys()))
            ))
        self.d_code = d_code
        print("{}".format(ds_error["initialize_ok"]))


class GlobalPositionSystem():
    def __init__(
            self,
            key: str = "ONE"
        ) -> None:
        """
        input:
            key: letter (for example 'N') to store a
            global position coordinate. default is 'ONE'.

        output:
            GlobalPositionSystem.d_code: dictionary of GlobalPositionSystem
            object related blender python code, structured in
            d_code['ls_code']: main part of the code packed as string list
            d_code['es_import']: import part of the code packed as string set

        description:
            Zerog GlobalPositionSystem code object to store a global position
            by pressing CTRL + SHIFT + choosen letter and
            later on teleport back to the position by ALT + chooen letter.
        """
        print("{}".format(ds_error["gps_initialize"]))
        # check that key is not shift or ctrl or alt as those are used for stor and recall
        s_key = key.upper()
        if (s_key == 'LEFT_SHIFT') or \
                (s_key == 'LEFT_CTRL') or \
                (s_key == 'LEFT_ALT'):
            # error
            sys.exit(
                "Error at zerogmodule.py GlobalPositionSystem.__init__: {}".format(
                    ds_error["gps_key"]
                )
            )
        else:
            self.d_code = {}  # type: Dict
            self.d_code.update({"es_import": {"import bpy"}})
            self.d_code.update({"ls_code": [
                "\n# Global Position Coordinate {}".format(s_key),
                "try:",
                "    bpy.context.scene.objects.active = bpy.data.objects['EmptyIch']",
                "except KeyError:",
                "    bpy.ops.object.empty_add(type='PLAIN_AXES')",
                "    bpy.context.active_object.name = 'EmptyIch'",
                "    bpy.context.scene.objects.active = bpy.data.objects['EmptyIch']",
                "# controller",
                "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlGpsStore{}')".format(s_key),
                "bpy.context.object.game.controllers['CtrlGpsStore{}'].mode = 'MODULE'".format(s_key),
                "bpy.context.object.game.controllers['CtrlGpsStore{}'].module = 'bgectrlrmodule.globalpositionstore'".format(s_key),
                "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlGpsRecall{}')".format(s_key),
                "bpy.context.object.game.controllers['CtrlGpsRecall{}'].mode = 'MODULE'".format(s_key),
                "bpy.context.object.game.controllers['CtrlGpsRecall{}'].module = 'bgectrlrmodule.globalpositionrecall'".format(s_key),
                "# sensor",
                "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensGpsStoreKey{}')".format(s_key),
                "bpy.context.object.game.sensors['SensGpsStoreKey{}'].key = '{}'".format(s_key, s_key),
                "bpy.context.object.game.sensors['SensGpsStoreKey{}'].modifier_key_1 = 'LEFT_SHIFT'".format(s_key),
                "bpy.context.object.game.sensors['SensGpsStoreKey{}'].modifier_key_2 = 'LEFT_CTRL'".format(s_key),
                "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensGpsRecallKey{}')".format(s_key),
                "bpy.context.object.game.sensors['SensGpsRecallKey{}'].key = '{}'".format(s_key, s_key),
                "bpy.context.object.game.sensors['SensGpsRecallKey{}'].modifier_key_1 = 'LEFT_ALT'".format(s_key),
                "# link",
                "bpy.context.object.game.sensors['SensGpsStoreKey{}'].link(bpy.context.object.game.controllers['CtrlGpsStore{}'])".format(s_key, s_key),
                "bpy.context.object.game.sensors['SensGpsRecallKey{}'].link(bpy.context.object.game.controllers['CtrlGpsRecall{}'])".format(s_key, s_key),
            ]})
        # output
        print("{}".format(ds_error["initialize_ok"]))


class Mesh():
    def __init__(
            self,
            relative_path_file: str,
            diffuse_color: Optional[Tuple[float, float, float]] = None,
            visibility_key: Optional[str] = None
        ) -> None:
        """
        input:
            realtive_path_file: relative path to mesh file.
                valid file formats are: stl,.

            diffuse_color: mesh color given as
                rgb (float, float, float) tuple.
                default is None which result in grayish colored object.

            visibility_key: letter (for example N) to be able to toggle the mesh
                visibility on and off durig runtime. default is None.

        output:
            Mesh.d_code: Mesh code object

        description:
            Zerog Mesh code object
        """
        print("{}".format(ds_error["mesh_initialize"]))
        self.d_code = {}  # type: Dict
        # handling file
        s_absolute_path_file = "/mnt/host/{}".format(relative_path_file)
        s_file = relative_path_file.split("/")[-1]
        s_filetype = relative_path_file.split(".")[-1]
        self.d_code.update({"es_import": {"import bpy","import re"}})
        self.d_code.update({"ls_code": [
            "\n# Mesh {}".format(s_file),
            "es_origin = set([obj.name for obj in bpy.data.objects])",
            "bpy.ops.import_mesh.{}(filepath='{}')".format(
                s_filetype,
                s_absolute_path_file),
            "bpy.context.active_object.name = re.sub('[^a-zA-Z0-9]+', '', bpy.context.active_object.name)",
            "es_load = set([obj.name for obj in bpy.data.objects])",
            "s_load = es_load.difference(es_origin).pop()",
        ]})
        # handling color
        if not (diffuse_color is None):
            self.d_code["es_import"].add("import bpy")
            self.d_code["ls_code"].extend([
                "# color",
                "bpy.context.scene.objects.active = bpy.data.objects[s_load]",
                "s_material = 'material{}'.format(len(bpy.data.materials))",
                "bpy.data.materials.new(s_material)",
                "bpy.data.materials[s_material].diffuse_color = {}".format(
                    diffuse_color
                ),
                "bpy.data.objects[s_load].data.materials.append(bpy.data.materials[s_material])",
            ])
        # handling visibility_key
        if not (visibility_key is None):
            self.d_code["es_import"].add("import bpy")
            self.d_code["ls_code"].extend([
                "# visibility",
                "bpy.context.scene.objects.active = bpy.data.objects[s_load]",
                "# controler",
                "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlToggleVisibility')",
                "bpy.context.object.game.controllers['CtrlToggleVisibility'].mode = 'MODULE'",
                "bpy.context.object.game.controllers['CtrlToggleVisibility'].module = 'bgectrlrmodule.visibilitytoggle'",
                "# sensor",
                "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensVisibilityKey')",
                "bpy.context.object.game.sensors['SensVisibilityKey'].key = '{}'".format(visibility_key.upper()),  # bue 20170708: missing f keys and numbers
                "# link",
                "bpy.context.object.game.sensors['SensVisibilityKey'].link(bpy.context.object.game.controllers['CtrlToggleVisibility'])",
            ])
        # output
        print("{}".format(ds_error["initialize_ok"]))


class Scene():
    def __init__(
            self,
            relative_path_file: str,
            mesh_list: List[str],
            diffuse_color_list: Optional[List[Tuple[float, float, float]]] = None,
            visibility_key_list: Optional[List[str]] = None,
            delete_object_list: Optional[List[str]] = None,
        ) -> None:
        """
        input:
            realtive_path_file: relative path to scene file.
                valid file formats are: x3d,.

            mesh_list: list of mesh names inside the scene.

            diffuse_color_list: list of mesh color given as
                rgb (float, float, float) tuple.
                default is None which result in grayish colored object.

            visibility_key_list: letter (for example N) to be able to toggle the mesh
                visibility on and off durig runtime. default is None.

            delete_object_list: list of scene objects to delete
                while importing the scene.
        output:
            Scene.d_code: Mesh code object

        description:
            Zerog Scene code object
        """
        print("{}".format(ds_error["scene_initialize"]))
        self.d_code = {}  # type: Dict
        # handling file
        s_absolute_path_file = "/mnt/host/{}".format(relative_path_file)
        s_file = relative_path_file.split("/")[-1]
        s_filetype = relative_path_file.split(".")[-1]
        self.d_code.update({"es_import": {"import bpy","import re"}})
        self.d_code.update({"ls_code": [
            "\n# Scene {}".format(s_file),
            "bpy.ops.import_scene.{}(filepath='{}')".format(
                s_filetype,
                s_absolute_path_file
            ),
        ]})
        # delete objects
        if not (delete_object_list  is None):
            self.d_code["es_import"].add("import bpy")
            self.d_code["ls_code"].extend([
                "for obj in bpy.data.objects:",
                "    obj.select = False",
                "for s_obj in {}:".format(delete_object_list),
                "    bpy.data.objects[s_obj].select = True",
                "bpy.ops.object.delete(use_global=True)",
            ])
        # for each mesh in scene
        for i, s_mesh in enumerate(mesh_list):
            # handling color
            if not (diffuse_color_list is None):
                if not (diffuse_color_list[i] is None):
                    self.d_code["es_import"].add("import bpy")
                    self.d_code["ls_code"].extend([
                        "# color",
                        "bpy.context.scene.objects.active = bpy.data.objects['{}']".format(
                            s_mesh
                        ),
                		"bpy.context.scene.objects.active.active_material.diffuse_color = {}".format(
                			diffuse_color_list[i]
                		),
                    ])
            # handling visibility_key
            if not (visibility_key_list is None):
                if not (visibility_key_list[i] is None):
                    self.d_code["es_import"].add("import bpy")
                    self.d_code["ls_code"].extend([
                        "# visibility",
                        "bpy.context.scene.objects.active = bpy.data.objects['{}']".format(
                            s_mesh
                        ),
                        "# controler",
                        "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlToggleVisibility')",
                        "bpy.context.object.game.controllers['CtrlToggleVisibility'].mode = 'MODULE'",
                        "bpy.context.object.game.controllers['CtrlToggleVisibility'].module = 'bgectrlrmodule.visibilitytoggle'",
                        "# sensor",
                        "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensVisibilityKey')",
                        "bpy.context.object.game.sensors['SensVisibilityKey'].key = '{}'".format(
                            visibility_key_list[i].upper()
                        ),
                        "# link",
                        "bpy.context.object.game.sensors['SensVisibilityKey'].link(bpy.context.object.game.controllers['CtrlToggleVisibility'])",
                    ])
        # output
        print("{}".format(ds_error["initialize_ok"]))


class Navigation():
    def __init__(
            self,
            speed: Optional[float] = 1,
            sight_distance: Optional[int] = 1024
        ) -> None:
        """
        input:
            sight_distance: integer to specify how fahr you can see.

        output:
            Navigation.ls_code: Navigation code object

        description:
            Zerog Navigation code object
        """
        print("{}".format(ds_error["navigation_initialize"]))
        self.d_code = {}  # type: Dict
        self.d_code.update({"es_import": {"import bpy", "import math"}})
        self.d_code.update({"ls_code": [
            "\n# Navigation",
            "# set camera clip ending",
            "bpy.context.scene.objects.active = bpy.data.objects['Camera']",
            "bpy.context.active_object.name = 'CameraIch'",
            "bpy.data.cameras['Camera'].clip_end = {}".format(sight_distance),
            "# parent camera with empty obj",
            "try:",
            "    bpy.context.scene.objects.active = bpy.data.objects['EmptyIch']",
            "except KeyError:",
            "    bpy.ops.object.empty_add(type='PLAIN_AXES')",
            "    bpy.context.active_object.name = 'EmptyIch'",
            "bpy.data.objects['CameraIch'].parent = bpy.data.objects['EmptyIch']",
            "bpy.context.scene.objects.active = bpy.data.objects['EmptyIch']",
            "bpy.data.objects['EmptyIch'].location=[0,0,0]",
            "bpy.data.objects['CameraIch'].location=[0,0,0]",
            "bpy.data.objects['CameraIch'].rotation_euler=[math.pi/2,0,0]",
            "for o_area in bpy.context.screen.areas:",
            "    if o_area.type == 'VIEW_3D':",
            "        o_area.spaces[0].region_3d.view_perspective = 'CAMERA'",
            "        break",
            "# controller",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlWatchUp')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlWatchDown')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlWatchLeft')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlWatchRight')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveUp')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveDown')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveForward')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveBackward')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveLeft')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlMoveRight')",
            "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlEmptyIchPosition')",
            "bpy.context.object.game.controllers['CtrlEmptyIchPosition'].mode = 'MODULE'",
            "bpy.context.object.game.controllers['CtrlEmptyIchPosition'].module = 'bgectrlrmodule.emptyichposition'",
            "# sensor",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensNotShift')",
            "bpy.context.object.game.sensors['SensNotShift'].key = 'LEFT_SHIFT'",
            "bpy.context.object.game.sensors['SensNotShift'].invert = True",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensNotCtrl')",
            "bpy.context.object.game.sensors['SensNotCtrl'].key = 'LEFT_CTRL'",
            "bpy.context.object.game.sensors['SensNotCtrl'].invert = True",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensNotAlt')",
            "bpy.context.object.game.sensors['SensNotAlt'].key = 'LEFT_ALT'",
            "bpy.context.object.game.sensors['SensNotAlt'].invert = True",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyWatchUp')",
            "bpy.context.object.game.sensors['SensKeyWatchUp'].key = 'W'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyWatchDown')",
            "bpy.context.object.game.sensors['SensKeyWatchDown'].key = 'S'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyWatchLeft')",
            "bpy.context.object.game.sensors['SensKeyWatchLeft'].key = 'A'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyWatchRight')",
            "bpy.context.object.game.sensors['SensKeyWatchRight'].key = 'D'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveUp')",
            "bpy.context.object.game.sensors['SensKeyMoveUp'].key = 'O'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveDown')",
            "bpy.context.object.game.sensors['SensKeyMoveDown'].key = 'L'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveForward')",
            "bpy.context.object.game.sensors['SensKeyMoveForward'].key = 'I'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveBackward')",
            "bpy.context.object.game.sensors['SensKeyMoveBackward'].key = 'K'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveLeft')",
            "bpy.context.object.game.sensors['SensKeyMoveLeft'].key = 'J'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyMoveRight')",
            "bpy.context.object.game.sensors['SensKeyMoveRight'].key = 'SEMI_COLON'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensEmptyIchPosition')",
            "bpy.context.object.game.sensors['SensEmptyIchPosition'].use_all_keys = True",
            "# actuator",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActWatchUp')",
            "bpy.context.object.game.actuators['ActWatchUp'].use_local_location = True",
            "bpy.context.object.game.actuators['ActWatchUp'].offset_rotation = (0.0074, 0.0, 0.0)",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActWatchDown')",
            "bpy.context.object.game.actuators['ActWatchDown'].use_local_location = True",
            "bpy.context.object.game.actuators['ActWatchDown'].offset_rotation = (-0.0074, 0.0, 0.0)",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActWatchLeft')",
            "bpy.context.object.game.actuators['ActWatchLeft'].use_local_location = True",
            "bpy.context.object.game.actuators['ActWatchLeft'].offset_rotation = (0.0, 0.0, 0.0074)",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActWatchRight')",
            "bpy.context.object.game.actuators['ActWatchRight'].use_local_location = True",
            "bpy.context.object.game.actuators['ActWatchRight'].offset_rotation = (0.0, 0.0, -0.0074)",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveUp')",
            "bpy.context.object.game.actuators['ActMoveUp'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveUp'].offset_location = (0.0, 0.0, {})".format(speed * 0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveDown')",
            "bpy.context.object.game.actuators['ActMoveDown'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveDown'].offset_location = (0.0, 0.0, {})".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveForward')",
            "bpy.context.object.game.actuators['ActMoveForward'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveForward'].offset_location = (0.0, {}, 0.0)".format(speed * 0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveBackward')",
            "bpy.context.object.game.actuators['ActMoveBackward'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveBackward'].offset_location = (0.0, {}, 0.0)".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveLeft')",
            "bpy.context.object.game.actuators['ActMoveLeft'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveLeft'].offset_location = ({}, 0.0, 0.0)".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActMoveRight')",
            "bpy.context.object.game.actuators['ActMoveRight'].use_local_location = True",
            "bpy.context.object.game.actuators['ActMoveRight'].offset_location = ({}, 0.0, 0.0)".format(speed * 0.10),
            "# link",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlWatchUp'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlWatchUp'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlWatchUp'])",
            "bpy.context.object.game.sensors['SensKeyWatchUp'].link(bpy.context.object.game.controllers['CtrlWatchUp'])",
            "bpy.context.object.game.actuators['ActWatchUp'].link(bpy.context.object.game.controllers['CtrlWatchUp'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlWatchDown'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlWatchDown'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlWatchDown'])",
            "bpy.context.object.game.sensors['SensKeyWatchDown'].link(bpy.context.object.game.controllers['CtrlWatchDown'])",
            "bpy.context.object.game.actuators['ActWatchDown'].link(bpy.context.object.game.controllers['CtrlWatchDown'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlWatchLeft'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlWatchLeft'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlWatchLeft'])",
            "bpy.context.object.game.sensors['SensKeyWatchLeft'].link(bpy.context.object.game.controllers['CtrlWatchLeft'])",
            "bpy.context.object.game.actuators['ActWatchLeft'].link(bpy.context.object.game.controllers['CtrlWatchLeft'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlWatchRight'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlWatchRight'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlWatchRight'])",
            "bpy.context.object.game.sensors['SensKeyWatchRight'].link(bpy.context.object.game.controllers['CtrlWatchRight'])",
            "bpy.context.object.game.actuators['ActWatchRight'].link(bpy.context.object.game.controllers['CtrlWatchRight'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveUp'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveUp'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveUp'])",
            "bpy.context.object.game.sensors['SensKeyMoveUp'].link(bpy.context.object.game.controllers['CtrlMoveUp'])",
            "bpy.context.object.game.actuators['ActMoveUp'].link(bpy.context.object.game.controllers['CtrlMoveUp'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveDown'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveDown'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveDown'])",
            "bpy.context.object.game.sensors['SensKeyMoveDown'].link(bpy.context.object.game.controllers['CtrlMoveDown'])",
            "bpy.context.object.game.actuators['ActMoveDown'].link(bpy.context.object.game.controllers['CtrlMoveDown'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveForward'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveForward'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveForward'])",
            "bpy.context.object.game.sensors['SensKeyMoveForward'].link(bpy.context.object.game.controllers['CtrlMoveForward'])",
            "bpy.context.object.game.actuators['ActMoveForward'].link(bpy.context.object.game.controllers['CtrlMoveForward'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveBackward'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveBackward'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveBackward'])",
            "bpy.context.object.game.sensors['SensKeyMoveBackward'].link(bpy.context.object.game.controllers['CtrlMoveBackward'])",
            "bpy.context.object.game.actuators['ActMoveBackward'].link(bpy.context.object.game.controllers['CtrlMoveBackward'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveLeft'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveLeft'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveLeft'])",
            "bpy.context.object.game.sensors['SensKeyMoveLeft'].link(bpy.context.object.game.controllers['CtrlMoveLeft'])",
            "bpy.context.object.game.actuators['ActMoveLeft'].link(bpy.context.object.game.controllers['CtrlMoveLeft'])",
            "bpy.context.object.game.sensors['SensNotShift'].link(bpy.context.object.game.controllers['CtrlMoveRight'])",
            "bpy.context.object.game.sensors['SensNotCtrl'].link(bpy.context.object.game.controllers['CtrlMoveRight'])",
            "bpy.context.object.game.sensors['SensNotAlt'].link(bpy.context.object.game.controllers['CtrlMoveRight'])",
            "bpy.context.object.game.sensors['SensKeyMoveRight'].link(bpy.context.object.game.controllers['CtrlMoveRight'])",
            "bpy.context.object.game.actuators['ActMoveRight'].link(bpy.context.object.game.controllers['CtrlMoveRight'])",
            "bpy.context.object.game.sensors['SensEmptyIchPosition'].link(bpy.context.object.game.controllers['CtrlEmptyIchPosition'])",
        ]})
        # output
        print("{}".format(ds_error["initialize_ok"]))


class Torch():
    def __init__(
            self,
            speed: Optional[float] = 1,
        ) -> None:
        """
        input: None

        output:
            Torch.d_code: Torch code object

        description:
            Zerog Torch code object
        """
        print("{}".format(ds_error["torch_initialize"]))
        self.d_code = {}  # type: Dict
        self.d_code.update({"es_import": {"import bpy"}})
        self.d_code.update({"ls_code": [
            "\n# Torch",
            "# rename lampe to torch",
            "bpy.context.scene.objects.active = bpy.data.objects['Lamp']",
            "bpy.context.active_object.name = 'Torch'",
            "# controller",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchUp')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchDown')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchForward')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchBackward')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchLeft')",
            "bpy.ops.logic.controller_add(type='LOGIC_AND', name='CtrlTorchRight')",
            "bpy.ops.logic.controller_add(type='PYTHON', name='CtrlTorchReset')",
            "bpy.context.object.game.controllers['CtrlTorchReset'].mode = 'MODULE'",
            "bpy.context.object.game.controllers['CtrlTorchReset'].module = 'bgectrlrmodule.torchreset'",
            "# sensor",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchUp')",
            "bpy.context.object.game.sensors['SensKeyTorchUp'].key = 'O'",
            "bpy.context.object.game.sensors['SensKeyTorchUp'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchDown')",
            "bpy.context.object.game.sensors['SensKeyTorchDown'].key = 'L'",
            "bpy.context.object.game.sensors['SensKeyTorchDown'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchForward')",
            "bpy.context.object.game.sensors['SensKeyTorchForward'].key = 'I'",
            "bpy.context.object.game.sensors['SensKeyTorchForward'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchBackward')",
            "bpy.context.object.game.sensors['SensKeyTorchBackward'].key = 'K'",
            "bpy.context.object.game.sensors['SensKeyTorchBackward'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchLeft')",
            "bpy.context.object.game.sensors['SensKeyTorchLeft'].key = 'J'",
            "bpy.context.object.game.sensors['SensKeyTorchLeft'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensKeyTorchRight')",
            "bpy.context.object.game.sensors['SensKeyTorchRight'].key = 'SEMI_COLON'",
            "bpy.context.object.game.sensors['SensKeyTorchRight'].modifier_key_1 = 'LEFT_SHIFT'",
            "bpy.ops.logic.sensor_add(type='KEYBOARD', name='SensTorchReset')",
            "bpy.context.object.game.sensors['SensTorchReset'].key = 'T'",
            "bpy.context.object.game.sensors['SensTorchReset'].modifier_key_1 = 'LEFT_SHIFT'",
            "# actuator",
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchUp')",
            "bpy.context.object.game.actuators['ActTorchUp'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchUp'].offset_location = (0.0, 0.0, {})".format(speed * 0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchDown')",
            "bpy.context.object.game.actuators['ActTorchDown'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchDown'].offset_location = (0.0, 0.0, {})".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchForward')",
            "bpy.context.object.game.actuators['ActTorchForward'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchForward'].offset_location = (0.0, {}, 0.0)".format(speed * 0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchBackward')",
            "bpy.context.object.game.actuators['ActTorchBackward'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchBackward'].offset_location = (0.0, {}, 0.0)".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchLeft')",
            "bpy.context.object.game.actuators['ActTorchLeft'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchLeft'].offset_location = ({}, 0.0, 0.0)".format(speed * -0.10),
            "bpy.ops.logic.actuator_add(type='MOTION', name='ActTorchRight')",
            "bpy.context.object.game.actuators['ActTorchRight'].use_local_location = True",
            "bpy.context.object.game.actuators['ActTorchRight'].offset_location = ({}, 0.0, 0.0)".format(speed * 0.10),
            "# link",
            "bpy.context.object.game.sensors['SensKeyTorchUp'].link(bpy.context.object.game.controllers['CtrlTorchUp'])",
            "bpy.context.object.game.actuators['ActTorchUp'].link(bpy.context.object.game.controllers['CtrlTorchUp'])",
            "bpy.context.object.game.sensors['SensKeyTorchDown'].link(bpy.context.object.game.controllers['CtrlTorchDown'])",
            "bpy.context.object.game.actuators['ActTorchDown'].link(bpy.context.object.game.controllers['CtrlTorchDown'])",
            "bpy.context.object.game.sensors['SensKeyTorchForward'].link(bpy.context.object.game.controllers['CtrlTorchForward'])",
            "bpy.context.object.game.actuators['ActTorchForward'].link(bpy.context.object.game.controllers['CtrlTorchForward'])",
            "bpy.context.object.game.sensors['SensKeyTorchBackward'].link(bpy.context.object.game.controllers['CtrlTorchBackward'])",
            "bpy.context.object.game.actuators['ActTorchBackward'].link(bpy.context.object.game.controllers['CtrlTorchBackward'])",
            "bpy.context.object.game.sensors['SensKeyTorchLeft'].link(bpy.context.object.game.controllers['CtrlTorchLeft'])",
            "bpy.context.object.game.actuators['ActTorchLeft'].link(bpy.context.object.game.controllers['CtrlTorchLeft'])",
            "bpy.context.object.game.sensors['SensKeyTorchRight'].link(bpy.context.object.game.controllers['CtrlTorchRight'])",
            "bpy.context.object.game.actuators['ActTorchRight'].link(bpy.context.object.game.controllers['CtrlTorchRight'])",
            "bpy.context.object.game.sensors['SensTorchReset'].link(bpy.context.object.game.controllers['CtrlTorchReset'])",
        ]})
        # output
        print("{}".format(ds_error["initialize_ok"]))
