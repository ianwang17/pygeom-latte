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
    bl = 12.19 # length
    bw = 5.49 # width
    bh = 2.44 # height

    lab_s = pg4.geant4.solid.Box("box_s", bl, bw, bh, registry = reg, lunit = "m") 
    lab_l = pg4.geant4.LogicalVolume(lab_s, "G4_AIR", "Lab_l", registry = reg)
    lab_pv = pg4.geant4.PhysicalVolume([0,0,0], [0,0,0], lab_l, "Lab_pv", world_l, registry = reg)

    # Now the concrete surrounding:
    # Make a filled concrete box of dimensions airbox + 1m, then subtract the airbox so that we are left with a 
    # hollow concrete shell.

    outer_conc = pg4.geant4.solid.Box("outer_conc", bl+1, bw+1, bh+1, reg, lunit="m")
    inner_conc = pg4.geant4.solid.Box("inner_conc", bl, bw, bh, reg, lunit="m")

    conc_s = pg4.geant4.solid.Subtraction("concrete", outer_conc, inner_conc, [[0,0,0], [0,0,0]], registry=reg)
    conc_l = pg4.geant4.LogicalVolume(conc_s, "G4_CONCRETE", "conc_l", registry=reg)
    #conc_l.pygeom_color_rgba = [122, 97, 110, 0.26]
    conc_pv = pg4.geant4.PhysicalVolume([0,0,0], [0,0,0], conc_l, "conc_pv", world_l, registry=reg)

    

    return reg

