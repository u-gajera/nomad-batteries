from nomad_batteries import BatteryApp
from nomad_batteries.main import generate_archives

from . import LOGGER


def test_resolve_ocv():
    battery_app = BatteryApp()
    archives = generate_archives(logger=LOGGER)
    battery_app.resolve_ocv(archives=archives, logger=LOGGER)
    assert True
    # add assertions here to check if `battery_app.open_circuit_voltage` is correct
