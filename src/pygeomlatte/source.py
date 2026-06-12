import pyg4ometry as pg4
import numpy as np
from pygeomtools.materials import LegendMaterialRegistry

def build_source(
    reg: pg4.geant4.Registry,
    materials: LegendMaterialRegistry,
    lar_l: pg4.geant4.LogicalVolume, 
    source_mat: str = "G4_Th",
    source_radius_mm: float = 280
    ) -> pg4.geant4.Registry:
    """ Build source guide tube, capsule, and source and place them into the registry. 

    Parameters
    -----------
    reg 
        The registry to add the fiber shroud to.
    materials
        The material registry to use to construct the fibers.
    lar_l
        Logical volume for the liquid argon you're placing the source into.
    source_mat
        The source material you want to simulate. Default is thorium. 
    source_radius_mm
        The radial position of the source and guide tube in the cryostat, in mm. Default is 280mm. 
    """
 
    bottom_height = 10.6 # bottom cylinder of source capsule 
    top_height = 7 # top cylinder of source capsule 

    tube_s = pg4.geant4.solid.Tubs("Tube_s", 5.85, 6.35, 658, 0, 2 * np.pi, registry=reg, lunit="mm") # thickness/diameter/length from Fusion model
    tube_l = pg4.geant4.LogicalVolume(tube_s, "G4_STAINLESS-STEEL", "Tube_l", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [source_radius_mm, 0, 0], tube_l, "Tube", lar_l, registry=reg)

    # source capsule - make bottom and top cylinders separately, then join using Union
    bottom_s = pg4.geant4.solid.Tubs("bottom_s", 0, 3.2, bottom_height, 0, 2 * np.pi, reg, 'mm')
    top_s = pg4.geant4.solid.Tubs("top_s", 0, 2, top_height, 0, 2 * np.pi, reg, 'mm')
    capsule_s = pg4.geant4.solid.Union("capsule_s", bottom_s, top_s, [[0,0,0], [0, 0, (bottom_height/2)+(top_height/2)-.1]], reg)
    capsule_l = pg4.geant4.LogicalVolume(capsule_s, "G4_STAINLESS-STEEL", "capsule_l", reg)
    pg4.geant4.PhysicalVolume([0,0,0], [source_radius_mm,0,0], capsule_l, "capsule_pv", lar_l, reg)

    # inside source capsule
    air_height = 4
    air_in_capsule_s = pg4.geant4.solid.Tubs("air_in_capsule_s", 0, 2, air_height, 0, 2 * np.pi, reg, "mm")
    air_in_capsule_l = pg4.geant4.LogicalVolume(air_in_capsule_s, "G4_AIR", "AirInCapsule_l", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, -(bottom_height/2)+(air_height/2)+2], air_in_capsule_l, "air_in_capsule_pv", capsule_l, registry=reg)

    source_s = pg4.geant4.solid.Tubs("Source_s", 0, 1, 2, 0, 2 * np.pi, registry=reg)
    source_l = pg4.geant4.LogicalVolume(source_s, source_mat, "Source_L", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], source_l, "Source", air_in_capsule_l, registry=reg)
    
    return reg
 
