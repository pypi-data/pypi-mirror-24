# Author: Lukas Snoek [lukassnoek.github.io]
# Contact: lukassnoek@gmail.com
# License: 3 clause BSD

from __future__ import absolute_import

from . import estimators
from . import core
from . import exp_model
from . import postproc
from . import feature_extraction
from . import feature_selection
from . import utils
from os.path import dirname, join
import os

__version__ = '0.3.3'

fsl = 'FSLDIR' in os.environ.keys()
if not fsl:
    msg = ("FSL does not seem to be installed. Skbold cannot "
           "perform any EPI/MNI transformations of patterns or masks!")
    print(msg)

data_path = join(dirname(dirname(utils.__file__)), 'data')
testdata_path = join(data_path, 'test_data')
roidata_path = join(data_path, 'ROIs')
harvardoxford_path = join(roidata_path, 'harvard_oxford')

__all__ = ['estimators', 'core', 'data', 'exp_model',
           'postproc', 'feature_extraction', 'utils',
           'harvardoxford_path', 'feature_selection']
