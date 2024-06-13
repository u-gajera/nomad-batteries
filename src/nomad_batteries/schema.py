import numpy as np
from typing import List
from structlog.stdlib import (
    BoundLogger,
)

from nomad.datamodel import EntryArchive
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Package, Quantity


m_package = Package()


class BatteryApp(ArchiveSection):
    open_circuit_voltage = Quantity(
        type=np.float64, description='Open circuit voltage of the battery'
    )

    def resolve_ocv(self, archives: List[EntryArchive], logger: BoundLogger):
        scf_archive = archives[0]
        deleted_atom_1_archive = archives[1]
        # add here the operations to resolve and assign `self.open_circuit_voltage` using the needed archives
        # ...


m_package.__init_metainfo__()
