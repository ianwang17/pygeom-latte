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
    # create the LAr volume for LATTE using cryostat length & radius from Fusion model

    # Added a primitive hollow cylinder with stainless steel
    inner_rad = 305.61 #mm
    outer_rad = 325 #mm
    height = 1500.1
    lid_thickness = 20 #mm

    flange_inner =  60 #mm
    flange_outer = 80 #mm
    flange_height = 60

    cryo_outer = pg4.geant4.solid.Tubs("cryo_outer", 0, outer_rad, height, 0, 2*np.pi, reg, lunit='mm')
    cryo_inner = pg4.geant4.solid.Tubs("cryo_inner", 0, inner_rad, height-lid_thickness, 0, 2*np.pi, reg, lunit='mm')
    cryo_wall = pg4.geant4.solid.Subtraction("cryo_wall", cryo_outer, cryo_inner, [[0,0,0], [0,0,0]], reg)

    top_flange = pg4.geant4.solid.Tubs("top_flange", flange_inner, flange_outer, flange_height, 0, 2*np.pi, reg, lunit='mm')
    flange_cutout = pg4.geant4.solid.Tubs("flange_cutout", 0, flange_inner, lid_thickness/2, 0, 2*np.pi, reg, lunit='mm')

    z_flange = height + flange_height
    cryo_with_flange = pg4.geant4.solid.Union("cryo_with_flange", cryo_wall, top_flange, [[0,0,0],[0,0,z_flange/2]], reg)
    
    
    crst_s = pg4.geant4.solid.Subtraction("crst_s", cryo_with_flange, flange_cutout, [[0,0,0], [0,0,z_flange/2]], reg)
    crst_l = pg4.geant4.LogicalVolume(crst_s, "G4_STAINLESS-STEEL", "crst_l", registry=reg)
    #crst_l.pygeom_color_rgba = [207, 212, 217, 0.01]
    crst_pv = pg4.geant4.PhysicalVolume([0,0,0], [0,0,0], crst_l, "crst", world_l, registry=reg)

    # Inside the cryostat should be liquid argon.
    lar_s = pg4.geant4.solid.Tubs("LAr_s", 0, 305.6, 1500, 0, 2 * np.pi, registry=reg, lunit="mm")
    lar_l = pg4.geant4.LogicalVolume(lar_s, materials.liquidargon, "LAr_l", registry=reg)
    lar_pv = pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], lar_l, "LAr", world_l, registry=reg)

    # Inside the cryostat should also be the copper IR shield and a 302SS funnel object.
    # Full locations of these two TBD. Need to ask Matthew/Jon

    # Implement of copper IR shield. 
    ir_inner = 63.5
    ir_outer = 305.61
    ir_thick = 10
    ir_loc = 350 
    irs_s = pg4.geant4.solid.Tubs("irs_s", ir_inner, ir_outer, ir_thick, 0, 2*np.pi, registry=reg, lunit="mm")
    irs_l = pg4.geant4.LogicalVolume(irs_s, "G4_Cu", "irs_l", registry=reg)
    irs_l.pygeom_color_rgba = [184, 115, 51, 0.05]
    irs_pv = pg4.geant4.PhysicalVolume([0,0,0], [0,0,ir_loc], irs_l, "irs", world_l, registry=reg)
    
    # Now for the funnel thingy. Use a cone with the top cut off. # Larger diam. 210m, inner 127mm
    lmin = 63.5 # lower inner radius
    lmax = 65 # lower outer radius
    umin = 103.5 # upper inner radius
    umax = 105 # upper outer radius
    guide_height = 100 # height of guide
    guide_loc = ir_loc+0.1 + guide_height/2 # location inside cryostat
    guide_s = pg4.geant4.solid.Cons("guide_s", lmin, lmax, umin, umax, guide_height, 0, 2*np.pi, reg, lunit='mm')
    guide_l = pg4.geant4.LogicalVolume(guide_s, "G4_STAINLESS-STEEL", "guide_l", registry=reg)
    guide_pv = pg4.geant4.PhysicalVolume([0,0,0],[0,0,guide_loc], guide_l, "guide", world_l, registry=reg)
    return reg

