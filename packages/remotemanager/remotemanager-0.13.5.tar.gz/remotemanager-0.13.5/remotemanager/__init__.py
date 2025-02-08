import os.path

from remotemanager.connection.computers.base import BaseComputer
from remotemanager.connection.computers.computer import Computer
from remotemanager.connection.url import URL
from remotemanager.dataset.dataset import Dataset
from remotemanager.decorators.remotefunction import RemoteFunction
from remotemanager.decorators.sanzufunction import SanzuFunction
from remotemanager.logging_utils.log import Handler
from remotemanager.script.script import Script

__all__ = [
    "Dataset",
    "URL",
    "RemoteFunction",
    "Computer",
    "Script",
    "BaseComputer",
    "SanzuFunction",
]  # noqa: F405
__version__ = "0.13.5"

# attach a global Logger to the manager
Logger = Handler()  # noqa: F405


# ipython magic
def load_ipython_extension(ipython):
    from remotemanager.decorators.magic import RCell

    ipython.register_magics(RCell)


def get_package_root() -> str:
    """returns the abspath to the package root directory"""
    return os.path.normpath(
        os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)
    )
