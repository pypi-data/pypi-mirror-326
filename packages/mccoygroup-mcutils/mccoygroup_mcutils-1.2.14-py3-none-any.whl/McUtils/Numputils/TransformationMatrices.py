
from .VectorOps import vec_normalize, vec_angles
import math, numpy as np, scipy as sp

__all__ = [
    "rotation_matrix",
    "skew_symmetric_matrix",
    "rotation_matrix_skew",
    "translation_matrix",
    "affine_matrix",
    "extract_rotation_angle_axis"
]

#######################################################################################################################
#
#                                                 rotation_matrix
#

def rotation_matrix_basic(xyz, theta):
    """rotation matrix about x, y, or z axis

    :param xyz: x, y, or z axis
    :type xyz: str
    :param theta: counter clockwise angle in radians
    :type theta: float
    """

    axis = xyz.lower()
    if axis == "z": # most common case so it comes first
        mat = [
            [ math.cos(theta), -math.sin(theta), 0.],
            [ math.sin(theta),  math.cos(theta), 0.],
            [ 0.,               0.,              1.]
        ]
    elif axis == "y":
        mat = [
            [ math.cos(theta), 0., -math.sin(theta)],
            [ 0.,              1.,               0.],
            [ math.sin(theta), 0.,  math.cos(theta)]
        ]
    elif axis == "x":
        mat = [
            [ 1.,               0.,               0.],
            [ 0.,  math.cos(theta), -math.sin(theta)],
            [ 0.,  math.sin(theta),  math.cos(theta)]
        ]
    else:
        raise Exception("{}: axis '{}' invalid".format('rotation_matrix_basic', xyz))
    return np.array(mat)

def rotation_matrix_basic_vec(xyz, thetas):
    """rotation matrix about x, y, or z axis

    :param xyz: x, y, or z axis
    :type xyz: str
    :param thetas: counter clockwise angle in radians
    :type thetas: float
    """

    thetas = np.asarray(thetas)
    nmats = len(thetas)
    z = np.zeros((nmats,))
    o = np.ones((nmats,))
    c = np.cos(thetas)
    s = np.sin(thetas)
    axis = xyz.lower()
    if axis == "z": # most common case so it comes first
        mat = [
            [ c, s, z],
            [-s, c, z],
            [ z, z, o]
        ]
    elif axis == "y":
        mat = [
            [ c, z, s],
            [ z, o, z],
            [-s, z, c]
        ]
    elif axis == "x":
        mat = [
            [ o, z, z],
            [ z, c, s],
            [ z,-s, c]
        ]
    else:
        raise Exception("{}: axis '{}' invalid".format('rotation_matrix_basic', xyz))
    return np.array(mat).T

#thank you SE for the nice Euler-Rodrigues imp: https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
def rotation_matrix_ER(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([
        [aa + bb - cc - dd, 2 * (bc + ad),     2 * (bd - ac)    ],
        [2 * (bc - ad),     aa + cc - bb - dd, 2 * (cd + ab)    ],
        [2 * (bd + ac),     2 * (cd - ab),     aa + dd - bb - cc]
    ])

def rotation_matrix_ER_vec(axes, thetas):
    """
    Vectorized version of basic ER
    """

    axes = vec_normalize(np.asanyarray(axes))
    thetas = np.asanyarray(thetas)
    # if len(axes.shape) == 1:
    #     axes = axes/np.linalg.norm(axes)
    #     axes = np.broadcast_to(axes, (len(thetas), 3))
    # else:
    #     axes = vec_normalize(axes)

    ax_shape = axes.shape[:-1]
    t_shape = thetas.shape
    axes = np.reshape(axes, (-1, 3))
    thetas = thetas.reshape(-1)
    if thetas.ndim == 0:
        base_shape = ax_shape
    elif axes.ndim == 1:
        base_shape = t_shape
    elif thetas.ndim != axes.ndim - 1:
        raise ValueError(f"can't broadcast axes and angles with shapes {ax_shape} and {t_shape}")
    else:
        base_shape = tuple(a if t == 1 else t for a,t in zip(ax_shape, t_shape))

    a = np.cos(thetas/2.0)
    b, c, d = np.moveaxis(-axes * np.reshape(np.sin(thetas / 2.0), (len(thetas), 1)), -1, 0)
    v = np.array([a, b, c, d])
    # triu_indices
    rows, cols = (
        np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 3]),
        np.array([0, 1, 2, 3, 1, 2, 3, 2, 3, 3])
    )
    aa, ab, ac, ad, bb, bc, bd, cc, cd, dd = v[rows] * v[cols]
    ## Uses half-angle formula to get compact form for Euler-Rodrigues
    # a^2 * I + [[ 0,    2ad, -2ac]   + [[b^2 - c^2 - d^2,               2bc,              2bd]
    #            [-2ad,    0,  2ab],     [             2bc, -b^2 + c^2 - d^2,              2cd]
    #            [ 2ac, -2ab,    0]]     [             2bd,              2cd, -b^2 - c^2 + d^2]]
    R = np.array([
        [aa + bb - cc - dd,      2 * (bc + ad),         2 * (bd - ac)],
        [    2 * (bc - ad),  aa - bb + cc - dd,         2 * (cd + ab)],
        [    2 * (bd + ac),      2 * (cd - ab),     aa - bb - cc + dd]
    ])
    R = np.moveaxis(R, -1, 0)

    return R.reshape(base_shape + (3, 3))

def rotation_matrix_align_vectors(vec1, vec2):
    angles, normals = vec_angles(vec1, vec2)
    return rotation_matrix(normals, angles)

def rotation_matrix(axis, theta):
    """
    :param axis:
    :type axis:
    :param theta: angle to rotate by (or Euler angles)
    :type theta:
    :return:
    :rtype:
    """

    try:
        flen = len(theta)
    except TypeError:
        flen = 0
    extra_shape = None

    if type(axis) == str:
        if flen >0:
            mat_fun = rotation_matrix_basic_vec
        else:
            mat_fun = rotation_matrix_basic
    else:
        if flen > 0:
            axis = np.asanyarray(axis)
            theta = np.asanyarray(theta)

            if axis.ndim == theta.ndim:
                if theta.ndim > 2:
                    extra_shape = theta.shape[:-2]
                    axis = axis.reshape((-1, 3))
                    theta = theta.reshape((-1, 3))
                mat_fun = rotation_matrix_align_vectors
            else:
                if theta.ndim > 1:
                    extra_shape = theta.shape
                    axis = axis.reshape((-1, 3))
                    theta = theta.reshape(-1)
                mat_fun = rotation_matrix_ER_vec
        else:
            mat_fun = rotation_matrix_ER

    mats = mat_fun(axis, theta)
    if extra_shape is not None:
        mats = mats.reshape(extra_shape + (3, 3))
    return mats

def skew_symmetric_matrix(upper_tri):
    upper_tri = np.asanyarray(upper_tri)
    l = len(upper_tri)
    n = int((1 + np.sqrt(1 + 8*l)) // 2)
    m = np.zeros((n, n))
    rows, cols = np.triu_indices_from(m, 1)
    m[rows, cols] =  upper_tri
    m[cols, rows] = -upper_tri
    return m

def extract_rotation_angle_axis(rot_mat):
    ang = np.arccos((np.trace(rot_mat) - 1)/2)
    skew = (rot_mat - rot_mat.T)/2
    ax = np.array([skew[2, 1], skew[0, 2], skew[1, 0]])
    n = np.linalg.norm(ax)
    return ang, ax/n

def youla_skew_decomp(A):
    n = len(A)
    s, T = sp.linalg.schur(A)

    l = np.diag(s, 1)
    if n % 2 == 0:
        start = 0
        end = n
    else:  # manage padding for odd dimension
        if abs(l[0]) < 1e-15:
            start = 1
            end = n
        else:
            start = 0
            end = n - 1
    l = l[start:end-1:2]
    cos = np.cos(l)
    sin = np.sin(l)

    # build 2x2 block mat
    U = np.eye(n)
    o = np.arange(start, end, 2)  # even inds
    e = np.arange(start + 1, end, 2)  # odd inds

    # print(start, end, l)

    U[o, o] = cos
    U[e, e] = cos
    U[o, e] = sin
    U[e, o] = -sin

    return U, T

def rotation_matrix_skew(upper_tri):
    A = skew_symmetric_matrix(upper_tri)
    # build Youla matrix
    U, T = youla_skew_decomp(A)
    return T@U@T.T

#######################################################################################################################
#
#                                                 translation_matrix
#

def translation_matrix(shift):
    share = np.asarray(shift)
    if len(share.shape) == 1:
        ss = share
        zs = 0.
        os = 1.
        mat = np.array(
            [
                [os, zs, zs, ss[0]],
                [zs, os, zs, ss[1]],
                [zs, zs, os, ss[2]],
                [zs, zs, zs, os   ]
            ]
        )
    else:
        zs = np.zeros((share.shape[0],))
        os = np.ones((share.shape[0],))
        ss = share.T
        mat = np.array(
            [
                [os, zs, zs, ss[0]],
                [zs, os, zs, ss[1]],
                [zs, zs, os, ss[2]],
                [zs, zs, zs, os   ]
            ]
        ).T
    return mat

#######################################################################################################################
#
#                                                 affine_matrix
#

def affine_matrix(tmat, shift):
    """Creates an affine transformation matrix from a 3x3 transformation matrix or set of matrices and a shift or set of vecs

    :param tmat: base transformation matrices
    :type tmat: np.ndarray
    :param shift:
    :type shift:
    :return:
    :rtype:
    """

    base_mat = np.asanyarray(tmat)
    if shift is None:
        return base_mat

    if base_mat.ndim > 2:
        shifts = np.asanyarray(shift)
        if shifts.ndim == 1:
            shifts = np.broadcast_to(shifts, (1,)*(base_mat.ndim-2) + shifts.shape)
        shifts = np.broadcast_to(shifts, base_mat.shape[:-2] + (3,))
        shifts = np.expand_dims(shifts, -1)
        mat = np.concatenate([base_mat, shifts], axis=-1)
        padding = np.array([0., 0., 0., 1.])
        padding = np.broadcast_to(
            np.broadcast_to(padding, (1,)*(base_mat.ndim-2) + padding.shape),
            mat.shape[:-2] + (4,)
        )
        padding = np.expand_dims(padding, -2)
        mat = np.concatenate([mat, padding], axis=-2)
    else:
        mat = np.concatenate([base_mat, shift[:, np.newaxis]], axis=-1)
        mat = np.concatenate([mat, [[0., 0., 0., 1.]]], axis=-2)
    return mat