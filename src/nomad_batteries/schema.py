# 0: Scf calculation
# 1: Octahydral Removal
# 2-8 Different movement of ion

import importlib
from typing import List, Optional, Literal, TYPE_CHECKING
from pydantic import BaseModel, Field
from nomad.metainfo import Quantity
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo import SimulationWorkflow
from nomad.normalizing.normalizer import Normalizer

# archive: Metadata:

from . import LOGGER

if TYPE_CHECKING:
    from nomad.metainfo import SchemaPackage
    from nomad.normalizing import Normalizer as NormalizerBaseClass
    from nomad.parsing import Parser as ParserBaseClass


# Defining the Battery schema
class BatterySchema(SimulationWorkflow):
    open_circuit_voltage: Quantity = Quantity(
        type=float, description='Open Circuit Voltage of the battery.'
    )


# Define the Normalizer/Finder for the battery plugin
class BatteryNormalizer(Normalizer):
    def my_normalize(self, archive: EntryArchive, logger=None):
        entries = archive.workflow2.tasks

        # Extract total energies
        total_energies = []
        for entry in entries:
            if 'scan-for-calculation' in entry.outputs:
                total_energy = entry.outputs[
                    'scan-for-calculation'
                ].section.energy.total.value
                total_energies.append(total_energy)

        # 0: Scf calculation
        # 1: Octahydral Removal
        # 2-8 Different movement of ion
        # Calculate properties
        def calculate_open_circuit_voltage(total_energies):
            """_summary_

            Args:
                total_energies (_type_): _description_

            Returns:
                _type_: _description_
            """
            # Example calculation (replace with actual formula as needed)
            return (total_energies[-1]) - (total_energies[0])

        def calculate_migration_barrier(total_energies):
            return max(total_energies[2:]) - (total_energies[1])

        if total_energies:
            archive.results.properties.open_circuit_voltage = (
                calculate_open_circuit_voltage(total_energies)
            )

        if total_energies:
            archive.results.properties.migration_barrier = calculate_migration_barrier(
                total_energies
            )


# Define the Normalizer entry point
class BatteryNormalizerEntryPoint(BaseModel):
    id: Optional[str] = Field(
        description='some unique identifier corresponding to the entry point name.'
    )
    entry_point_type: Literal['battery_normalizer'] = Field(
        'normalizer', description='Determines the entry point type.'
    )
    normalizer_class_name: str = Field(
        description='The fully qualified name of the Python class that implements the normalizer.'
    )

    def load(self) -> 'NormalizerBaseClass':
        module_name, class_name = self.normalizer_class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        normalizer_class = getattr(module, class_name)
        return normalizer_class


# Define the Plugin entry points
class BatteryPlugin(BaseModel):
    name: str = Field(description='Battery schemas')
    version: Optional[str] = Field(description='Plugin package version.0.1')
    entry_points: List[str] = Field(
        description='List of entry point ids contained in this package.'
    )


# Example plugin registration (replace with actual registration mechanism)
battery_plugin = BatteryPlugin(
    name='Battery Plugin',
    version='0.1',
    entry_points=[
        BatteryNormalizerEntryPoint(
            id='id_number',
            normalizer_class_name='tests.test_schema.BatteryNormalizer',
        ),
    ],
)


# Add the plugin (replace with actual method to add the plugin)
def add_battery_plugin():
    from nomad.config import config

    config.plugins.entry_points.options['battery'] = battery_plugin


add_battery_plugin()
