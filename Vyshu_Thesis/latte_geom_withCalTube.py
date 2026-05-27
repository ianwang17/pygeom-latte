import pygeoml1000 as l1000geom
from pygeoml1000 import core, hpge_strings
import pyg4ometry as pg4
from pathlib import Path
import yaml
import json
from dbetto import AttrsDict
import numpy as np
import pygeomtools

# converter: https://onlineyamltools.com/convert-yaml-to-json

sm_pathName = " " #string of path to special metadata yaml file
cm_pathName = " " #string of path channel map json file

special_metadata_path = Path(sm_pathName)
channelmap_path = Path(cm_pathName)

with open(special_metadata_path, "r") as f:
    special_metadata = AttrsDict(yaml.safe_load(f))
with open(channelmap_path, "r") as f:
    channelmap = AttrsDict(json.load(f))


distances_mm = [280]#, 95, 100, 110, 130, 150]
source_materials = ['G4_Th'] #["G4_Th", 'G4_Am', 'G4_Ba']
source_names = ['228Th'] #['228Th', '241Am', '133Ba'] # calibration sources


for index, source_mat in enumerate(source_materials): # looping through each of the source types
    for calibration_xpos in distances_mm: # looping through each of the distances from the center

        reg = pg4.geant4.Registry() # new registry each loop because same names can't be repeated in the same registry
        materials = l1000geom.core.materials.OpticalMaterialRegistry(reg)

        world_s = pg4.geant4.solid.Orb("World_s", 2500, registry=reg, lunit="mm")
        world_l = pg4.geant4.LogicalVolume(world_s, "G4_Galactic", "World", registry=reg)
        reg.setWorld(world_l)

        #config dictionary with channel map & special metadata
        config={
            "channelmap": channelmap, # holds location info about 
            "special_metadata": special_metadata,
        }

        # detail tells which parts of legend geometry to create/omit, can set this in special metadata yaml file
        detail = special_metadata["detail"]["radiogenic"] # cosmogenic or radiogenic
        instr = core.InstrumentationData(world_l, None, 0, 0, materials, reg, channelmap, special_metadata, AttrsDict(config), detail)

        # create the LAr volume for LATTE using cryostat length & radius from Fusion model
        lar_s = pg4.geant4.solid.Tubs("LAr_s", 0, 305.6, 1500, 0, 2 * np.pi, registry=reg, lunit="mm")
        lar_l = pg4.geant4.LogicalVolume(lar_s, instr.materials.liquidargon, "LAr_l", registry=reg)
        lar_pv = pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], lar_l, "LAr", world_l, registry=reg)

        # vaccuum instead of LAr, uncomment this & comment our LAr volume code
        # vacuum_s = pg4.geant4.solid.Orb("vacuum_s", 2000, registry=reg, lunit="mm")
        # vacuum_l = pg4.geant4.LogicalVolume(vacuum_s, 'G4_Galactic', "vacuum_l", registry=reg)
        # vacuum_pv = pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], vacuum_l, "Vacuum", world_l, registry=reg)
        # lar_l = vacuum_l

        instr = instr._replace(mother_lv=lar_l, mother_pv=lar_pv, mother_z_displacement=0)
        # print(instr)
        hpge_strings.place_hpge_strings(instr)
        # fiber length is set to 1349 mm
        # l1000geom.fibers.place_fiber_modules(instr) # doesn't work without overlap with one string

        core._assign_common_copper_surface(instr)

        ############################################# fibers #############################################

        fiber_radius = 60

        # dimensions from l1000 fibers.py 
        # layers in order: core, inner cladding, outer cladding, tbp coating
        tbp_thickness = .001093 # mm
        tpb_s = pg4.geant4.solid.Tubs("tpb_s", fiber_radius, fiber_radius+1+(2*tbp_thickness), 658, 0, 2 * np.pi, registry=reg, lunit="mm")
        tpb_l = pg4.geant4.LogicalVolume(tpb_s, materials.tpb_on_fibers, "tpb_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], tpb_l, "tpb", lar_l, registry=reg)

        outer_cladding_s = pg4.geant4.solid.Tubs("outer_cladding_s", fiber_radius+tbp_thickness, fiber_radius+tbp_thickness+1, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
        outer_cladding_l = pg4.geant4.LogicalVolume(outer_cladding_s, materials.pmma_out, "outer_cladding_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], outer_cladding_l, "outer_cladding", tpb_l, registry=reg)

        inner_cladding_s = pg4.geant4.solid.Tubs("inner_cladding_s", fiber_radius+tbp_thickness+0.02, fiber_radius+tbp_thickness+0.02+0.96, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
        inner_cladding_l = pg4.geant4.LogicalVolume(inner_cladding_s, materials.pmma, "inner_cladding_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], inner_cladding_l, "inner_cladding", outer_cladding_l, registry=reg)

        fiber_core_s = pg4.geant4.solid.Tubs("fiber_core_s", fiber_radius+tbp_thickness+0.02+0.04, fiber_radius+tbp_thickness+0.02+0.04+0.88, 658, 0, 2 * np.pi, registry=reg, lunit="mm")
        fiber_core_l = pg4.geant4.LogicalVolume(fiber_core_s, materials.ps_fibers, "fiber_core_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], fiber_core_l, "fiber_core", inner_cladding_l, registry=reg)
        

        ############################# source capsule/tube ###########################################################
    
        bottom_height = 10.6 # bottom cylinder of source capsule 
        top_height = 7 # top cylinder of source capsule 

        tube_s = pg4.geant4.solid.Tubs("Tube_s", 5.85, 6.35, 658, 0, 2 * np.pi, registry=reg, lunit="mm") # thickness/diameter/length from Fusion model
        tube_l = pg4.geant4.LogicalVolume(tube_s, "G4_STAINLESS-STEEL", "Tube_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [calibration_xpos, 0, 0], tube_l, "Tube", lar_l, registry=reg)

        # source capsule - make bottom and top cylinders separately, then join using Union
        bottom_s = pg4.geant4.solid.Tubs("bottom_s", 0, 3.2, bottom_height, 0, 2 * np.pi, reg, 'mm')
        top_s = pg4.geant4.solid.Tubs("top_s", 0, 2, top_height, 0, 2 * np.pi, reg, 'mm')
        capsule_s = pg4.geant4.solid.Union("capsule_s", bottom_s, top_s, [[0,0,0], [0, 0, (bottom_height/2)+(top_height/2)-.1]], reg)
        capsule_l = pg4.geant4.LogicalVolume(capsule_s, "G4_STAINLESS-STEEL", "capsule_l", reg)
        pg4.geant4.PhysicalVolume([0,0,0], [calibration_xpos,0,0], capsule_l, "capsule_pv", lar_l, reg)

        # inside source capsule
        air_height = 4
        air_in_capsule_s = pg4.geant4.solid.Tubs("air_in_capsule_s", 0, 2, air_height, 0, 2 * np.pi, reg, "mm")
        air_in_capsule_l = pg4.geant4.LogicalVolume(air_in_capsule_s, "G4_AIR", "AirInCapsule_l", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, -(bottom_height/2)+(air_height/2)+2], air_in_capsule_l, "air_in_capsule_pv", capsule_l, registry=reg)

        source_s = pg4.geant4.solid.Tubs("Source_s", 0, 1, 2, 0, 2 * np.pi, registry=reg)
        source_l = pg4.geant4.LogicalVolume(source_s, source_mat, "Source_L", registry=reg)
        pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], source_l, "Source", air_in_capsule_l, registry=reg)

        # write code from registry into gdml file named based on tube x position & calibration source
        pygeomtools.write_pygeom(reg, f"{source_names[index]}_{calibration_xpos}mm.gdml")
        print(f"{source_names[index]}_{calibration_xpos}mm.gdml") # quick check what files should've been created


# visualizer:

# fibers_color = [144, 238, 144, 0.1]
# viewer = pg4.visualisation.VtkViewerColoured(defaultColour=[0.1,0.1,0.1],
#                                              materialVisOptions={str(materials.liquidargon): [67, 169, 224, 0.1],
#                                              "G4_STAINLESS-STEEL": [90, 72, 138,.5],
#                                              str(materials.pmma): fibers_color,
#                                              str(materials.pmma_out): fibers_color,
#                                              str(materials.ps_fibers): fibers_color,
#                                              str(materials.tpb_on_fibers): fibers_color,
#                                              "G4_Th": [255, 0, 0, 1]})
# viewer.addLogicalVolume(reg.getWorldVolume())
# viewer.view()
