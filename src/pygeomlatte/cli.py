from __future__ import annotations

import argparse
import logging

from dbetto import TextDB, utils
import pygeomtools.geometry

from . import _version, core

log = logging.getLogger(__name__)

def dump_gdml_cli(argv: list[str] | None = None) -> None:
    args, config = _parse_cli_args(argv)
    logging.basicConfig()
    if args.verbose:
            logging.getLogger("pygeomlatte").setLevel(logging.DEBUG)
    if args.debug: 
        logging.root.setLevel(logging.DEBUG)
    
    registry = core.construct(config=config)

    log.info("Exportng GDML geometry to %s", args.filename)
    pygeomtools.write_pygeom(registry, args.filename)


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
        "--config",
        required=True,
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

    return args, config
