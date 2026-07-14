import pygeoml1000 as l1000geom
from pygeoml1000 import core, hpge_strings
import pyg4ometry as pg4
from pyg4ometry import geant4
from pygeomtools.materials import LegendMaterialRegistry

from pathlib import Path
import yaml
import json
import dbetto
from dbetto import AttrsDict
import numpy as np
import pygeomtools
import logging

from pygeomlatte.lab    import build_lab
from pygeomlatte.cryo   import build_cryo
from pygeomlatte.fibers import build_fibers
from pygeomlatte.source import build_source

log = logging.getLogger(__name__)

def construct(config: str | dict | None = None) -> geant4.Registry:

    """ Construct the LATTE geometry and return the registry containing the world volume. 
    
    Parameters
    -----------
    config
        Configuration dictionary (or the file containing it) defining relevant parameters of the geometry.
        This should have the following structure::

            input_files:
                sm_path: /path/to/special/metadata/yaml
                cm_path: /path/to/channel/map/json       
        
            source:
                source_mat: G4_Th, G4_Ba, etc.
                source_radius_mm: 280

            fiber_shroud:
                radius_in_mm: 60

    """             

    if isinstance(config, str):
        config = dbetto.utils.load_dict(config) 


    sm_pathName = config["input_files"]["sm_path"]
    cm_pathName = config["input_files"]["cm_path"]

    special_metadata_path = Path(sm_pathName)
    channelmap_path = Path(cm_pathName)

    with open(special_metadata_path, "r") as f:
            special_metadata = AttrsDict(yaml.safe_load(f))
    with open(channelmap_path, "r") as f:
            channelmap = AttrsDict(json.load(f))

    reg = pg4.geant4.Registry()
    materials = l1000geom.core.materials.OpticalMaterialRegistry(reg)
    
    world_s = pg4.geant4.solid.Orb("World_s", 2500, registry=reg, lunit="mm")
    world_l = pg4.geant4.LogicalVolume(world_s, "G4_Galactic", "World", registry=reg)
    reg.setWorld(world_l)
    #config dictionary with channel map & special metadata
    config_chmap={
        "channelmap": channelmap, # holds location info about 
        "special_metadata": special_metadata,
    }

        # detail tells which parts of legend geometry to create/omit, can set this in special metadata yaml file
    detail = special_metadata["detail"]["radiogenic"] # cosmogenic or radiogenic
    instr = core.InstrumentationData(world_l, None, 0, 0, materials, reg, channelmap, special_metadata, AttrsDict(config), detail)


    # I added this code, check to see if I need to add the extra definitions of the l and pv vols.
    reg = build_lab(reg, materials, world_l)


    reg = build_cryo(reg, materials, world_l)
    lar_l = reg.logicalVolumeDict["LAr_l"] # need this to place the HPGe strings and fibers.
    lar_pv = reg.physicalVolumeDict["LAr"] # need this to place the HPGe strings and fibers.

    
    #We're using the L1000 geometry method to place the HPGe string, we just need to tell it that our LAr volume is the volume it should use first.
    instr = instr._replace(mother_lv=lar_l, mother_pv=lar_pv, mother_z_displacement=0)
    hpge_strings.place_hpge_strings(instr)
    
    core._assign_common_copper_surface(instr)
    
    reg = build_fibers(reg, materials, lar_l, config["fiber_shroud"]["radius_in_mm"])

    reg = build_source(reg, materials, lar_l, config["source"]["source_mat"], config["source"]["source_radius_mm"])

    return reg
    
