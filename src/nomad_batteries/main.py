"""
This module should be part of a more ellaborated process. We will fake the workflow using the tests/data as filepaths,
but in reality, NOMAD needs to query this information and combine it somehow. This means that the `workflow_archives`
should be resolved in another way, and not by specifying by hand the path. We have to combine different
entries following the folder structure:
.
└── material-A/
    ├── SCF files >> OUTCAR (GeomOpt)
    ├── 01/ (one atom removed)
    │   ├── OUTCAR (ISIF=2, this is an electronic relax, not ionic!)
    │   ├── 001/ (another atom removed)
    │   │   └── OUTCAR (ISIF=2)
    │   ├── 002/
    │   │   └── OUTCAR (ISIF=2)
    │   └── 003/
    │       └── OUTCAR (ISIF=2)
    ├── 02/
    │   ├── OUTCAR (ISIF=2)
    │   ├── 001/
    │   │   └── OUTCAR (ISIF=2)
    │   ├── 002/
    │   │   └── OUTCAR (ISIF=2)
    │   └── 003/
    │       └── OUTCAR (ISIF=2)
    ├── 03/
    │   ├── OUTCAR (ISIF=2)
    │   ├── 001/
    │   │   └── OUTCAR (ISIF=2)
    │   ├── 002/
    │   │   └── OUTCAR (ISIF=2)
    │   └── 003/
    │       └── OUTCAR (ISIF=2)
    └── ...

The workflow entry should look like:
    ((SCF entry))   --> ((01 entry))    --> ((001 entry))
                                        --> ((002 entry))
                                        --> ((003 entry))
                    --> ((O2 entry))    --> ((001 entry))
                                        --> ((002 entry))
                                        --> ((003 entry))
                    --> ((03 entry))
"""

import os
from typing import List
from structlog.stdlib import (
    BoundLogger,
)

from nomad import utils
from nomad.datamodel import EntryArchive
from electronicparsers.vasp import VASPParser
from nomad.client.processing import normalize_all

# This `logger` will be passed anyways in a different way
logger = utils.get_logger(__name__)


def generate_archives(logger: BoundLogger = logger) -> List[EntryArchive]:
    # Defining paths to the testing files
    current_dir = os.path.dirname(os.path.abspath(__file__))  # go to directory
    relative_filepaths = [
        '../../tests/data/AlCo2S4/OUTCAR',
        '../../tests/data/AlCo2S4/neb/01/OUTCAR',
        '../../tests/data/AlCo2S4/neb/02/OUTCAR',
        '../../tests/data/AlCo2S4/neb/03/OUTCAR',
        '../../tests/data/AlCo2S4/neb/04/OUTCAR',
        '../../tests/data/AlCo2S4/neb/05/OUTCAR',
    ]
    filepaths = [
        os.path.normpath(os.path.join(current_dir, rel_file))
        for rel_file in relative_filepaths
    ]

    archives = []
    parser = VASPParser()
    for filepath in filepaths:
        archive = EntryArchive()
        parser.parse(filepath=filepath, archive=archive, logger=logger)
        archives.append(archive)
        normalize_all(entry_archive=archive, logger=logger)
    return archives
