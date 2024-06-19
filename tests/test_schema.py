from nomad.datamodel import EntryArchive

from nomad_batteries import BatteriesSchema
from pydantic import BaseModel, Field
from nomad.metainfo import Quantity


class BatteryNormalizer(self):
    schema = BatteriesSchema()
    schema.normalize(EntryArchive(), LOGGER)
    assert True
