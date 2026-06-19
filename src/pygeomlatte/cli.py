from __future__ import annotations

import argparse
import logging

from dbetto import TextDB, utils
from pyg4ometry import config as meshconfig
import pygeomtools.geometry
from pygeomtools.materials import LegendMaterialRegistry

from . import _version, core

log = logging.getLogger(__name__)

def dump_gdml_cli(argv: list[str] | None = None) -> None:
    args, config = _parse_cli_args(argv)
    logging.basicConfig()
    if args.verbose:
            logging.getLogger("pygeomlatte").setLevel(logging.DEBUG)
    if args.debug: 
        logging.root.setLevel(logging.DEBUG)
    
    vis_scene = {}
    if isinstance(args.visualize, str):
        vis_scene = utils.load_dict(args.visualize)

    registry = core.construct(config=config)

    #if args.print_volumes:
    #    geometry.print_volumes(registry, args.print_volumes)

    if args.filename is not None:
        log.info("Exportng GDML geometry to %s", args.filename)
        pygeomtools.write_pygeom(registry, args.filename)

    if args.visualize:
        log.info("visualizing...")
        fibers_color = [144, 238, 144, 0.1]
        viewer = pg4.visualisation.VtkViewerColoured(
            defaultColour=[0.1,0.1,0.1], 
            materialVisOptions={str(materials.liquidargon): [67, 169, 224, 0.1],
            "G4_STAINLESS-STEEL": [90, 72, 138,.5],
            str(materials.pmma): fibers_color,
            str(materials.pmma_out): fibers_color,
            str(materials.ps_fibers): fibers_color,
            str(materials.tpb_on_fibers): fibers_color,
            "G4_Th": [255, 0, 0, 1]})
        viewer.addLogicalVolume(reg.getWorldVolume())
        viewer.view()

def _parse_cli_args(argv: list[str] | None = None) -> tuple[argparse.Namespace, dict]:
    parser = argparse.ArgumentParser(
        prog="pygeom-latte",
        description="%(prog)s command line interface",
    )
    # global options
    parser.add_argument(
        "--version",
        action="version",
        help="""Print %(prog)s version and exit""",
        version=_version.__version__,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="""Increase the program verbosity""",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="""Increase the program verbosity to maximum""",
    )
    parser.add_argument(
        "--visualize",
        const=True,
        nargs="?",
        help="""Open a VTK visualization of the generated geometry""",
    )
    parser.add_argument(
        "--config",
        action="store",
        help="""Select a config file to read geometry info from.""",
    )
    parser.add_argument(
        "filename",
        default="output.gdml",
        nargs="?",
        help="""File name for the output GDML geometry.""",
    )

    args = parser.parse_args(argv)

    config = utils.load_dict(args.config)

    if not args.visualize and args.filename == "":
        parser.error("No output file and no visualization specified.")

    return args, config
