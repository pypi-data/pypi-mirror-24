###
# file: zerog.py
#
# language: python3
# version: 4.
# date: 2017-05-06
# author: bue
# licernse: GPL>=3
#
# run:
#    import zerogravity.zerog as g
#
# description:
#    main zerogravity library
#
# requirements:
#    python > 3.6
#    64 bit operating system Linux, MacOS or Windows
###

import platform
import docker  # >=2.0
import importlib.util
import json
import os
import re
import requests
import shutil
import sys
from typing import Set, Union
from zerogravity.zerogmodule import Code, GlobalPositionSystem, Mesh, Navigation, Scene, Torch

# get zerogravity root directory
s_zerog_rootdir = "{}/".format(importlib.util.find_spec(
    "zerogravity"
).submodule_search_locations[0])
s_zerog_rootdir = s_zerog_rootdir.replace("\\","/")
if (platform.system() == "Windows"):
    ls_pwd_absolute_host = os.getcwd().split("\\")
    s_drive = ls_pwd_absolute_host.pop(0)  # C:
    s_drive = s_drive.replace(":","").lower()
    s_pwd_absolute_host = "/".join(ls_pwd_absolute_host)
    s_pwd_absolute_host = "/{}/{}/".format(s_drive, s_pwd_absolute_host)
else:
    s_pwd_absolute_host = "{}/".format(os.getcwd())

# error handling
with open(
        "{}error.json".format(
            s_zerog_rootdir,
        )) as f_json:
    ds_error = json.load(f_json)


# plugin classes
# moved to zerogmodule.py

# basic class
class zeroGblender():
    """ zeroGblender main object """

    def __init__(self) -> None:
        """
        item:
            zeroGblender.blender_version: blender version used by ZeroGblender.
                automatically detetced.

            zeroGblender.blenderplayer_path: local path to
                Windows and MacOS blenderplayer. automatically detected.

            zeroGblender.zerog_objects: zerog Mesh or other objects added with
                self.add()

            zeroGblender.zerog_os: the operating system
                blender should render for.
                default is the os zeroGbelnder is executed.
                valid options are:
                + 'Darwin': MacOS
                + 'Linux': Linux
                + 'Windows': Windows

        description:
            initialize zeroGblender object
        """
        print("{}".format(ds_error["zerogblender_initialize"]))
        self.zerog_object: Set[Union[
            Code,
            GlobalPositionSystem,
            Mesh,
            Navigation,
            Scene,
            Torch,
        ]] = set()  # empty object set
        self.zerog_os = platform.system()  # get operating system
        self.docker_client = docker.from_env()  # get  docker client
        try:
            self.docker_client.ping()
            # build zerogravity image
            try:
                self.docker_client.images.build(
                    path=s_zerog_rootdir,  # docker file directory
                    tag="zerogravity:latest",
                    quiet=False,
                    nocache=False,
                    rm=False,
                    pull=True,
                    forcerm=True,
                )
            except docker.errors.BuildError:
                print("{}".format(ds_error["internet_connection_no"]))
            # get blender version
            s_blender_version = self.docker_client.containers.run(
                image="zerogravity", command="blender --version", remove=True)
            self.blender_version = re.sub(
                r"[^a-zA-Z0-9_]", "",
                s_blender_version.decode(encoding="utf-8"),
            )
            # get blender player directory
            self.blenderplayer_path = "{}/bplayer/{}".format(
                s_zerog_rootdir,
                self.blender_version,
            )
            if not (os.path.exists(self.blenderplayer_path)):
                sys.exit(
                    "Error at zerog.py zeroGblender.__init__: {}".format(
                        ds_error["blenderplayer_missing"].format(
                            self.blender_version,
                            self.blenderplayer_path,
                        )
                    )
                )
        except requests.ConnectionError:
            sys.exit(
                "Error at zerogravity zeroGblender.__init__: {}".format(
                    ds_error["docker_daemon_run"],
                )
            )
        # output
        print("{}".format(ds_error["initialize_ok"]))


    def add(self, zerog_object: Union[
            Code,
            GlobalPositionSystem,
            Mesh,
            Navigation,
            Scene,
            Torch,
        ]) -> None:
        """
        input:
            zerog_object: zerog object to be added to zeroGblender object

        description:
            add Mesh or other object to zeroGblender object
        """
        self.zerog_object.add(zerog_object)


    def __bpy_code(self, game_name: str) -> str:
        """
        input:
            game_name: filename string with or without extension

        output:
            s_pwd_absolute_container: docker container realted current working directory path

        description:
            write  zeroGcode.py blender python code file into
            current work directory.
        """
        # set generic path and filenames
        s_outputpathpart = "/mnt/host/{}".format(game_name)
        s_path_bplayer = "/usr/local/lib/bplayer/{}/".format(
            self.blender_version,
        )
        s_blendfile = "{}.blend".format(game_name)

        # set os specific path and filenames
        if (self.zerog_os == "Linux"):
            s_bplayer = "/usr/bin/blenderplayer"
            s_gamefile = "{}.game".format(game_name)
        elif (self.zerog_os == "Darwin"):
            s_bplayer = "{}blenderplayer.app".format(s_path_bplayer)
            s_gamefile = "{}.app".format(game_name)

        elif (self.zerog_os == "Windows"):
            s_bplayer = "{}blenderplayer.exe".format(s_path_bplayer)
            s_gamefile = "{}.exe".format(game_name)
        else:
            sys.exit(
                "Error at zerog.py zeroGblender.__bpy_code: {}".format(
                        ds_error["os_unknown"].format(self.zerog_os)
                    )
                )

        # handle code
        ls_code = ["# zerogravity generated blender python file\n",]
        # import code
        es_import = {"import bpy", "import glob", "import os", "import shutil"}
        for o_zerog in self.zerog_object:
            [es_import.add(s_import) for s_import in o_zerog.d_code['es_import']]
        ls_import = list(es_import)
        ls_import.sort()
        ls_code.extend(ls_import)
        # delete Cube
        ls_code.extend([
            "for obj in bpy.data.objects:",
            "    obj.select = False",
            "bpy.data.objects['Cube'].select = True",
            "bpy.ops.object.delete(use_global=True)",
        ])
        # module code
        for o_zerog in self.zerog_object:
            ls_code.extend(o_zerog.d_code['ls_code'])
        # render code
        ls_code.extend([
            "\n# make output dir",
            "try:",
            "    os.mkdir('{}Blender/')".format(
                s_outputpathpart,
            ),
            "except FileExistsError:",
            "    pass",
            "try:",
            "    os.mkdir('{}{}/')".format(
                s_outputpathpart,
                self.zerog_os,
            ),
            "except FileExistsError:",
            "    pass",
            "\n# save blend file",
            "bpy.ops.wm.save_mainfile(filepath='{}Blender/{}')".format(
                s_outputpathpart,
                s_blendfile,
            ),
            "\n# render game",
            "bpy.ops.wm.addon_enable(module='game_engine_save_as_runtime')",
            "bpy.ops.wm.save_as_runtime(player_path='{}', filepath='{}{}/{}', copy_python=True)".format(
                s_bplayer,
                s_outputpathpart,
                self.zerog_os,
                s_gamefile,
            ),
            "\n# copy bge ctrler module file",
            "shutil.copyfile('/usr/local/lib/zgravity/bgectrlrmodule.py', '{}Blender/bgectrlrmodule.py')".format(
                s_outputpathpart,
            ),
            "shutil.copyfile('/usr/local/lib/zgravity/bgectrlrmodule.py', '{}{}/bgectrlrmodule.py')".format(
                s_outputpathpart,
                self.zerog_os,
            ),
        ])
        # only for mac os render code
        if (self.zerog_os == "Darwin"):
            ls_code.extend([
                "shutil.copyfile('/usr/local/lib/zgravity/bgectrlrmodule.py', '{}{}/{}/Contents/Resources/bgectrlrmodule.py')".format(
                    s_outputpathpart,
                    self.zerog_os,
                    s_gamefile,
                ),
            ])
        # only for windows os render code
        if (self.zerog_os == "Windows"):
            ls_code.extend([
                "\n# replace python lib",
                "s_source = glob.glob('/usr/local/lib/bplayer/*/lib/')[0]",
                "s_sink = glob.glob('/mnt/host/*Windows/*/python/lib/')[0]",
                "shutil.rmtree(s_sink)",
                "ls_sink = s_sink.split('/')",
                "ls_sink.pop(-1)",
                "s_sink = '/'.join(ls_sink)",
                "shutil.copytree(s_source, s_sink)",
                "\n# copy dynamic link libraries",
                "for s_file in os.listdir('{}'):".format(
                    s_path_bplayer,
                ),
                "    if re.search(r'.+\.dll', s_file) and not(os.path.isfile('{}Windows/{{}}'.format(s_file))):".format(
                    s_outputpathpart,
                ),
                "        shutil.copy('{}{{}}'.format(s_file), '{}Windows/')".format(
                    s_path_bplayer,
                    s_outputpathpart,
                ),
            ])
        # write code to file
        s_codefile = "zeroGcode{}.py".format(
            self.zerog_os,
        )
        with open(s_codefile, "w", newline="") as f_out:  # pwd
            for s_code in ls_code:
                s_code += "\n"
                f_out.write(s_code)
        # output
        return(s_codefile)


    def blend_game(self, game_name: str = "zeroGgame", b_debug: bool = False) -> None:
        """
        input:
            game_name: this definds the output folder and output file prefix.
                default is zeroGgame.
            b_debug:

        output: blend file and renderd game for the self.zerog_os specified
            operating system.

        description:
            render blender game
        """
        print("{}".format(ds_error["zerogblender_blend_game"]))

        # generate blender python code file
        s_codefile = self.__bpy_code(game_name=game_name)

        # build container instance and run the python code
        if (b_debug):
            self.docker_client.containers.run(
                image="zerogravity",
                command="blender --background --python /mnt/host/{} 2>&1".format(
                    s_codefile,
                ),
                remove=False,
                volumes={s_pwd_absolute_host: {"bind": "/mnt/host", "mode": "rw"}}
            )
        else:
            self.docker_client.containers.run(
                image="zerogravity",
                command="blender --background --python /mnt/host/{}".format(
                    s_codefile,
                ),
                remove=True,
                volumes={s_pwd_absolute_host: {"bind": "/mnt/host", "mode": "rw"}}
            )

        # output
        print("{}".format(ds_error["render_ok"].format(game_name)))
