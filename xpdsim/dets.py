""" Spoof detectors """
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Christopher J. Wright
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from cycler import cycler
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
import os
import bluesky.examples as be

DATA_DIR = rs_fn('xpdsim', 'data/')


class PutGet:
    """basic class to have set/put method"""

    def __init__(self, numeric_val=1):
        self._val = numeric_val

    def put(self, val):
        """set value"""
        self._val = val
        return self._val

    def get(self):
        """read current value"""
        return self._val


class SimulatedCam:
    """class to simulate Camera class"""

    def __init__(self, frame_acq_time=0.1, acquire=1):
        # default acq_time = 0.1s and detector is turned on
        self.acquire_time = PutGet(frame_acq_time)
        self.acquire = PutGet(acquire)


# define simulated PE1C
class SimulatedPE1C(be.ReaderWithFileStore):
    """Subclass the bluesky plain detector examples ('Reader');

    also add realistic attributes.
    """

    def __init__(self, name, read_fields, fs, **kwargs):
        self.images_per_set = PutGet()
        self.number_of_sets = PutGet()
        self.cam = SimulatedCam()
        self._staged = False
        super().__init__(name, read_fields, fs=fs, **kwargs)
        self.ready = True  # work around a hack in Reader


def build_image_cycle(path):
    """Build image cycles, essentially generators with endless images

    Parameters
    ----------
    path: str
        Path to the files to be used as the base for the cycle, this can
        include some globing

    Returns
    -------
    Cycler:
        The iterable like object to cycle through the images
    """
    imgs = ImageSequence(os.path.join(path, '*.tif*'))
    return cycler(pe1_image=[i for i in imgs])


nsls_ii_path = os.path.join(DATA_DIR, 'XPD/ni/')

chess_path = os.path.join(DATA_DIR, 'chess/')


def det_factory(name, fs, path, **kwargs):
    """Build a detector using real images

    Parameters
    ----------
    name: str
        Name of the detector
    fs: filestore.FileStore instance
        The filestore to save all the data in
    path: str
        The path to the tiff files

    Returns
    -------
    detector: SimulatedPE1C instance
        The detector
    """
    cycle = build_image_cycle(
        path)
    gen = cycle()

    def nexter():
        return next(gen)['pe1_image']

    return SimulatedPE1C(name,
                         {'pe1_image': lambda: nexter()}, fs=fs, **kwargs)