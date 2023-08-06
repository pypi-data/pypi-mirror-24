from . layout import Circle, Matrix, POV, Strip, Cube, font
from . layout.geometry import Rotation
from . layout.geometry.matrix import gen_matrix
from . layout.geometry.circle import gen_circle
from . layout.geometry.cube import gen_cube
from . import animation, colors, layout, util
from . util import log
from . util import image

from . colors import gamma
from . drivers import return_codes
from . project import data_maker
from . project.project import read_project

# These are DEPRECATED
from . layout import LEDCircle, LEDMatrix, LEDPOV, LEDStrip, LEDCube
from . layout import matrix_drawing as matrix


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(abspath(__file__)), 'VERSION')
    return open(filename).read().strip()


__version__ = _get_version()
VERSION = __version__
