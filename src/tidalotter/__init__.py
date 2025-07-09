"""
The easy TIDAL download client!
"""

try:
    from importlib.metadata import version
    __version__ = version("tidalotter")
except ImportError:
    __version__ = "unknown"
__author__ = "ItsThatOneJack"
__email__ = "jack@itoj.dev"

from .main import downloadTrack

__all__ = ["downloadTrack"]