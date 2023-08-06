###
# file: bgectrlrmodule.py
#
# language: python3
# version: 4.
# date: 2017-05-06
# author: bue
# licernse: GPL>=3
#
# run:
#    import bgectrlrmodule
#
# description:
#    blender python controller modules for zerogravity.zerogravitymodules
###

# bue 20170716: never import bpy. the belnderplayer can not import bpy
import bge

def emptyichposition(o_ctrlr):
    """
    input bender logic:
        EmptyIch
        controller type='PYTHON' mode='MODULE' name='CtrlEmptyIchPosition'
        sensor type='ALWAYS' name='SensEmptyIchPosition'

    description:
        store curnet global position
    """
    print("store current global position: {}".format(o_ctrlr.owner.worldPosition))
    bge.logic.globalDict.update({'EmptyIchPosition': tuple(o_ctrlr.owner.worldPosition)})  # get position via controller


def globalpositionrecall(o_ctrlr):
    """
    input bender logic:
        EmptyIch
        controller type='PYTHON' mode='MODULE' name='CtrlGpsRecallN'
        sensor type='KEYBOARD' name='SensGpsRecallKeyN' key='' first_modifier =''

    description:
        recall a stored global position
    """
    bge.logic.loadGlobalDict()
    s_key = o_ctrlr.sensors[0].key  # get sensor key  via controller
    try:
        o_ctrlr.owner.worldPosition = bge.logic.globalDict['GlobalPositionSystem']["{}".format(s_key)]  # set position via controller
        print("recall global position: {} {}".format(s_key, o_ctrlr.owner.worldPosition))
    except KeyError:
        pass


def globalpositionstore(o_ctrlr):
    """
    input bender logic:
        EmptyIch
        controller type='PYTHON' mode='MODULE' name='CtrlGpsStoreN'
        sensor type='KEYBOARD' name='SensGpsStoreKeyN' key='' first_modifier =''

    description:
        store curnet global position
    """
    s_key = o_ctrlr.sensors[0].key  # get sensor key  via controller
    print("store global position: {} {}".format(s_key, o_ctrlr.owner.worldPosition))
    bge.logic.globalDict.update({'GlobalPositionSystem': {"{}".format(s_key): tuple(o_ctrlr.owner.worldPosition)}})  # get position via controller
    bge.logic.saveGlobalDict()


def torchreset(o_ctrlr):
    """
    input bender logic:
        Torch
        controller type='PYTHON' mode='MODULE' name='CtrlTorchReset'
        sensor type='KEYBOARD' name='SensTorchReset' key='T' first_modifier ='SHIFT_LEFT'

    description:
        store curnet global position
    """
    o_ctrlr.owner.worldPosition = bge.logic.globalDict['EmptyIchPosition'] # set current position via controlle
    print("reset torch position: {}".format(o_ctrlr.owner.worldPosition))


def visibilitytoggle(o_ctrlr):
    """
    input blender logic:
        Mesh
        controller type='PYTHON' mode='MODULE'
        sensor type='KEYBOARD' name='VisibilityKey'

    description:
        togglel controller.owner object between visible and invisible
    """
    if (o_ctrlr.sensors["SensVisibilityKey"].positive):
        for _ in o_ctrlr.sensors["SensVisibilityKey"].events:
            if (o_ctrlr.owner.visible == True):  # was visible
                o_ctrlr.owner.visible = False
                print("visibility : {} off".format(o_ctrlr.sensors["SensVisibilityKey"].key))
            else:  # was invisible
                o_ctrlr.owner.visible = True
                print("visibility : {} on".format(o_ctrlr.sensors["SensVisibilityKey"].key))
