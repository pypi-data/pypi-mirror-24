# Basic Mvp class, from which first-level specific (e.g. FSL or, perhaps in the
# future, SPM) containers/converters are subclassed.

# Author: Lukas Snoek [lukassnoek.github.io]
# Contact: lukassnoek@gmail.com
# License: 3 clause BSD

from __future__ import print_function, absolute_import, division

import os
import nibabel as nib
import os.path as op
import numpy as np
from glob import glob
from copy import copy
from sklearn.externals import joblib


class Mvp(object):
    """
    Mvp (multiVoxel Pattern) class.
    Creates an object, specialized for storing fMRI data that will be analyzed
    using machine learning or RSA-like analyses, that stores both the data
    (X: an array of samples by features, y: numeric labels corresponding to
    X's classes/conditions) and the corresponding meta-data (e.g. nifti header,
    mask info, etc.).

    Parameters
    ----------
    X : ndarray
        A 2D numpy-array with rows indicating samples and
        columns indicating features.
    y : list or ndarray
        Array/list with labels/targets corresponding to samples in X.
    mask : str
        Absolute path to nifti-file that will mask (index) the patterns.
    mask_thres : int or float
        Minimum value for mask (in cases of probabilistic masks).

    Attributes
    ----------
    mask_shape : tuple
        Shape of mask that patterns will be indexed with.
    nifti_header : Nifti1Header object
        Nifti-header from corresponding mask.
    affine : ndarray
        Affine corresponding to nifti-mask.
    voxel_idx : ndarray
        Array with integer-indices indicating which voxels are used in the
        patterns relative to whole-brain space. In other words, it allows to
        map back the patterns to a whole-brain orientation.
    X : ndarray
        The actual patterns (2D: samples X features)
    y : list or ndarray
        Array/list with labels/targets corresponding to samples in X.

    Notes
    -----
    This class is mainly meant to serve as a parent-class for ``MvpWithin``
    and ``MvpBetween``, but it can alternatively be used as an object to store
    a 'custom' multivariate-pattern set with meta-data.
    """

    def __init__(self, X=None, y=None, mask=None, mask_thres=0):

        if isinstance(mask, list):
            msg = 'You can only pass one mask! To use custom masks for each ' \
                  'source entry, specify the mask-key in source.'
            raise ValueError(msg)

        if mask is None:
            self.common_mask = None
            self.voxel_idx = None
        else:
            maskl = nib.load(mask)
            self.common_mask = {'path': mask, 'threshold': mask_thres,
                                'idx': (maskl.get_data() > mask_thres).ravel(),
                                'shape': maskl.shape, 'affine': maskl.affine}
            self.voxel_idx = np.arange(np.prod(self.common_mask['shape']))
            self.voxel_idx = self.voxel_idx[self.common_mask['idx']]

        self.nifti_header = None
        self.affine = None

        self.X = X
        self.y = y

    def write(self, path=None, name='mvp', backend='joblib'):
        """ Writes the Mvp-object to disk.

        Parameters
        ----------
        path : str
            Absolute path where the file will be written to.
        name : str
            Name of to-be-written file.
        backend : str
            Which format will be used to save the files. Default is 'joblib',
            which conveniently saves the Mvp-object as one file. Alternatively,
            and if the Mvp-object is too large to be save with joblib, a
            data-header format will be used, in which the data (``X``) will be
            saved using Numpy and the meta-data (everythin except ``X``) will
            be saved using joblib.
        """
        if path is None:
            path = os.getcwd()

        fn = op.join(path, name)

        print("Saving file '%s' to disk." % fn)

        if backend == 'joblib':
            try:
                joblib.dump(self, fn + '.jl', compress=3)
            except:
                msg = "Array too large to save with joblib; using Numpy ... "
                print(msg)
                backend = 'numpy'
                to_remove = glob(op.join(path, '*npy.z'))
                _ = [os.remove(f) for f in to_remove]

        if backend == 'numpy':
            np.save(fn + '_data.npy', self.X)
            self.X = None
            joblib.dump(self, fn + '_header.jl', compress=3)

    def update_mask(self, mask, threshold=0):
        # For external use

        if isinstance(mask, (str, unicode)):
            mask = nib.load(mask).get_data() > threshold

        if isinstance(mask, list):

            if not isinstance(threshold, list):
                threshold = [threshold] * len(mask)

            if all(isinstance(m, (str, unicode)) for m in mask):
                mask = [nib.load(copy(m)).get_data() > threshold[i]
                        for i, m in enumerate(mask)]

            to_iterate = zip(copy(mask), copy(threshold),
                             np.unique(self.featureset_id))
            unpack = True
        else:
            to_iterate = np.unique(self.featureset_id)
            unpack = False

        indices = []

        for it in to_iterate:

            if unpack:
                mask, threshold, i = it
            else:
                i = it

            fids = np.unique(self.featureset_id)
            posidx = np.where(i == fids)[0][0]
            tmp = np.zeros(self.data_shape[posidx]).ravel()
            fidx = self.featureset_id == i
            tmp[self.voxel_idx[fidx]] = 1
            tmp[mask.ravel()] += 1
            indices.append((tmp == 2)[self.voxel_idx[fidx]])

        indices = np.concatenate(indices, axis=0)
        self.X = self.X[:, indices]
        self.featureset_id = self.featureset_id[indices]
        self.voxel_idx = self.voxel_idx[indices]

    def _update_mask_info(self, mask, threshold=None):

        thr = 0 if threshold is None else threshold
        maskl = nib.load(mask)
        self.common_mask = {'path': mask, 'threshold': thr,
                            'idx': (maskl.get_data() > thr).ravel(),
                            'shape': maskl.shape, 'affine': maskl.affine}

        self.voxel_idx = np.arange(np.prod(self.common_mask['shape']))
        self.voxel_idx = self.voxel_idx[self.common_mask['idx']]
        self.affine = maskl.affine
        self.nifti_header = maskl.header
