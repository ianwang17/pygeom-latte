import numpy as np
import pyg4ometry as pg4
from pygeomtools.materials import LegendMaterialRegistry

def build_lab(
        reg: pg4.geant4.Registry,
        materials: LegendMaterialRegistry,
        world_l: pg4.geant4.LogicalVolume
    ) -> pg4.geant4.Registry:
    """
    Build lab room (Chapman 050) and place into the World registry. It's just
    a box of air with the dimensions of the lab surrounded by 1 meter of concrete
    on each side. The LATTE apparatus sits on the floor.

    Parameters:
    ----------------------
    reg 
        The registry to add the fiber shroud to.
    materials
        The material registry to use to construct the room.
    world_l
        Logical world volume that you'll place the room into. 

    """
    # Chapman 050 Room Dimensions (in meters)
    bl = 5#12.19 # length
    bw = 4#5.49 # width
    bh = 2#2.44 # height

    walls_s = pg4.geant4.solid.Box("walls_s", bl+1, bw+1, bh+1, reg, lunit='m')
    walls_l = pg4.geant4.LogicalVolume(walls_s, "G4_CONCRETE", "conc_l", registry=reg)
    #conc_l.pygeom_color_rgba = [122, 97, 110, 0.26]
    lab_walls = pg4.geant4.PhysicalVolume([0,0,0], [0,0,0], walls_l, "lab_walls", world_l, registry=reg)

    air_s = pg4.geant4.solid.Box("air_s", bl, bw, bh, registry = reg, lunit = "m") 
    air_l = pg4.geant4.LogicalVolume(air_s, "G4_AIR", "air_l", reg)
    air_pv = pg4.geant4.PhysicalVolume([0,0,0], [0,0,0], air_l, "air_pv", walls_l, registry = reg)
    


    return reg

