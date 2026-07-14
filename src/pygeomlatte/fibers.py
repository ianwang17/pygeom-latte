import pyg4ometry as pg4
import numpy as np
from pygeomtools.materials import LegendMaterialRegistry

def build_fibers(
    reg: pg4.geant4.Registry,
    materials: LegendMaterialRegistry,
    lar_l: pg4.geant4.LogicalVolume, 
    fiber_shroud_radius: float = 60
    ) -> pg4.geant4.Registry:
    """ Build fiber shroud and place it into the registry. Uses simplified fiber geometry (for now). 

    Parameters
    -----------
    reg 
        The registry to add the fiber shroud to.
    materials
        The material registry to use to construct the fibers.
    lar_l
        Logical volume for the liquid argon you're placing the source into.
    fiber_shroud_radius
        The radius of the fiber shroud "tube." HPGe detectors are inside the tube. 
    """
 
    # dimensions from l1000 fibers.py 
    # layers in order: core, inner cladding, outer cladding, tbp coating
    tbp_thickness = .001093 # mm
    tpb_s = pg4.geant4.solid.Tubs("tpb_s", fiber_shroud_radius, fiber_shroud_radius+1+(2*tbp_thickness), 658, 0, 2 * np.pi, registry=reg, lunit="mm")
    tpb_l = pg4.geant4.LogicalVolume(tpb_s, materials.tpb_on_fibers, "tpb_l", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], tpb_l, "tpb", lar_l, registry=reg)

    outer_cladding_s = pg4.geant4.solid.Tubs("outer_cladding_s", fiber_shroud_radius+tbp_thickness, fiber_shroud_radius+tbp_thickness+1, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
    outer_cladding_l = pg4.geant4.LogicalVolume(outer_cladding_s, materials.pmma_out, "outer_cladding_l", registry=reg)
    outer_cladding_l.pygeom_color_rgba = [221, 255, 221, 0.1]
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], outer_cladding_l, "outer_cladding", tpb_l, registry=reg)

    inner_cladding_s = pg4.geant4.solid.Tubs("inner_cladding_s", fiber_shroud_radius+tbp_thickness+0.02, fiber_shroud_radius+tbp_thickness+0.02+0.96, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
    inner_cladding_l = pg4.geant4.LogicalVolume(inner_cladding_s, materials.pmma, "inner_cladding_l", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], inner_cladding_l, "inner_cladding", outer_cladding_l, registry=reg)

    fiber_core_s = pg4.geant4.solid.Tubs("fiber_core_s", fiber_shroud_radius+tbp_thickness+0.02+0.04, fiber_shroud_radius+tbp_thickness+0.02+0.04+0.88, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
    fiber_core_l = pg4.geant4.LogicalVolume(fiber_core_s, materials.ps_fibers, "fiber_core_l", registry=reg)
    pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], fiber_core_l, "fiber_core", inner_cladding_l, registry=reg)
        
    return reg


