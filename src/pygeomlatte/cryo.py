import pyg4ometry as pg4
import numpy as np
import pygeoml1000 as l1000geom
from pygeomtools.materials import LegendMaterialRegistry

def build_cryo(
    reg: pg4.geant4.Registry,
    materials: LegendMaterialRegistry,
    world_l: pg4.geant4.LogicalVolume
    ) -> pg4.geant4.Registry:
    """ Build cryostat and place it into the registry. Right now it's just a cylinder of LAr. 

    Parameters
    -----------
    reg 
        The registry to add the fiber shroud to.
    materials
        The material registry to use to construct the fibers.
    world_l
        Logical world volume that you'll place the cryostat into. 
    """
    # need to add metal cryostat to this file
 
    # create the LAr volume for LATTE using cryostat length & radius from Fusion model

    lar_s = pg4.geant4.solid.Tubs("LAr_s", 0, 305.6, 1500, 0, 2 * np.pi, registry=reg, lunit="mm")
    lar_l = pg4.geant4.LogicalVolume(lar_s, materials.liquidargon, "LAr_l", registry=reg)
    lar_pv = pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], lar_l, "LAr", world_l, registry=reg)

    return reg

