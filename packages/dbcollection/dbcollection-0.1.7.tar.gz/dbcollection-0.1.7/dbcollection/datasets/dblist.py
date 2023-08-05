"""
Datasets list.

All available datasets must be added in this file.
"""


#---------------------------------------------------------
# List of image processing datasets
#---------------------------------------------------------

from . import coco
from . import cifar, pascal, mnist, imagenet
from . import caltech, inria
from . import flic, leeds_sports_pose, mpii_pose
from . import ucf


human_action = {
    "ucf_101": ucf.ucf101.UCF101,
    "ucf_sports": ucf.ucfsports.UCFSports
}

human_pose = {
    "flic": flic.Flic,
    "leeds_sports_pose": leeds_sports_pose.lsp.LSP,
    "leeds_sports_pose_extended": leeds_sports_pose.lsp_extended.LSPe,
    "mpii_pose": mpii_pose.MPIIPose
}

object_classification = {
    "cifar10": cifar.cifar10.Cifar10,
    "cifar100": cifar.cifar100.Cifar100,
    "ilsvrc2012": imagenet.ilsvrc2012.ILSVRC2012,
    'mnist': mnist.MNIST,
    "pascal_voc_2007": pascal.voc_2007.PascalVOC2007,
    "pascal_voc_2012": pascal.voc_2012.PascalVOC2012,
    "coco": coco.COCO
}

pedestrian_detection = {
    "caltech_pedestrian": caltech.pedestrian.Pedestrian,
    "inria_pedestrian": inria.pedestrian.Pedestrian
}


#---------------------------------------------------------
# MAIN list
#---------------------------------------------------------

datasets = {}
datasets.update(object_classification) # object classification
datasets.update(human_action) # human action
datasets.update(pedestrian_detection) # pedestrian detection/recognition
datasets.update(human_pose) # human pose



#---------------------------------------------------------
# Other functions
#---------------------------------------------------------

def fetch_default_task_name(name):
    """Returns the real task name associated to the default tag."""
    assert name, 'Must provide a name for the dataset.'
    return datasets[name].default_task


def dataset_tasks(name):
    """Returns a list of available tasks for a dataset."""
    assert name, 'Must provide a name for the dataset.'
    constructor = datasets[name]
    db_loader = constructor('nan', 'nan', False, False)  # init with empty data
    tasks = sorted(db_loader.get_all_tasks())
    tasks.remove('default')
    return tasks


def available_datasets():
    """
    Returns a dictionary with all the available datasets and
    their available tasks.
    """
    out = {}
    for db_name in sorted(datasets):
        out[db_name] = dataset_tasks(db_name)
    return out
