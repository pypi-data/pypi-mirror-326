#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geoclide.basic import Vector, Point, Normal
import math
import numpy as np


def dot(a, b):
    """
    The dot/scalar product

    Definition of the dot product:
    - (a . b) = a.x*b.x + a.y*b.y + a.z*b.z
    - (a . b) = ||a|| * ||b|| * cos(θ)

    Parameters
    ----------
    a : Vector | Normal
        The first vector or normal used for the dot product
    b : Vector | Normal
        The second vector or normal used for the dot product
    
    Results
    -------
    out : float
        The result of the dot product i.e. sum of products

    Examples
    --------
    >>> import geoclide as gc
    >>> a = gc.Vector(0., 0., 1.)
    >>> b = gc.Vector(math.sqrt(2.)/2., 0., math.sqrt(2.)/2.)
    >>> gc.dot(a,b)
    0.7071067811865476
    """
    if (isinstance(a, Vector) or isinstance(a, Normal)) and \
       (isinstance(b, Vector) or isinstance(b, Normal)):
        return (a.x*b.x + a.y*b.y + a.z*b.z)
    else:
        raise ValueError('Only Vector or Normal parameters are accepted')


def cross(a, b):
    """
    The cross product

    - /!\\ The cross product of 2 normals is not allowed

    Definition of the cross product:
    - (a × b) = ((a.y*b.z)-(a.z*b.y))x̂ + ((a.z*b.x)-(a.x*b.z))ŷ + ((a.x*b.y)-(a.y*b.x))*ẑ
    - (a × b) = ||a|| * ||b|| * sin(θ)

        where x̂, ŷ and ẑ are the unitary vectors respectively in axes x, y and z

    Parameters
    ----------
    a : Vector | Normal
        The first vector or normal used for the cross product
    b : Vector | Normal
        The second vector or normal used for the cross product
    
    Results
    -------
    out : Vector
        The result of the cross product

    Examples
    --------
    >>> import geoclide as gc
    >>> a = gc.Vector(0.,0.,1.)
    >>> b = gc.Vector(1.,0.,0.)
    >>> gc.cross(a,b)
    Vector(0.0, 1.0, 0.0)
    """
    if ( (isinstance(a, Vector) and isinstance(b, Vector)) or 
         (isinstance(a, Vector) and isinstance(b, Normal)) or 
         (isinstance(a, Normal) and isinstance(b, Vector)) ):
        return Vector((a.y*b.z)-(a.z*b.y), (a.z*b.x)-(a.x*b.z), (a.x*b.y)-(a.y*b.x))
    elif isinstance(a, Normal) and isinstance(b, Normal):
        raise ValueError('Only 1 Normal is tolerated not 2')
    else:
        raise ValueError('Only Vector or Normal parameters are accepted')
    

def normalize(v):
    """
    Normalize a Vector/Normal

    Parameters
    ----------
    v : Vector | Normal
        The Vector or Normal to be normalized
    
    Results
    -------
    out : Vector | Normal
        The normalized vector/normal

    Examples
    --------
    >>> import geoclide as gc
    >>> v = gc.Vector(1.,0.,1.)
    >>> gc.normalize(v)
    Vector(0.7071067811865475, 0.0, 0.7071067811865475)
    """
    if isinstance(v, Vector) or isinstance(v, Normal):
        return v / v.length()
    else:
        raise ValueError('The parameter v must be a Vector or Normal')


def coordinate_system(v1, method="m2"):
    """
    Create an orthogonal coordinate system from 1 vector (v1)

    Parameters
    ----------
    v1 : Vector
        The base vector used to create the orthogonal coordinate system
    method: str, optional
        Default is 'm2' (method from pbrt v4), other choice is 'm1' (pbrt v2 and v3)
    
    Results
    -------
    v2 : Vector
        The second vector of the orthogonal coordinate system
    v3 : Vector
        The third vector of the orthogonal coordinate system
    
    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(0., 0., 1.)
    >>> v2, v3 = gc.coordinate_system(v1)
    (Vector(1.0, -0.0, -0.0), Vector(-0.0, 1.0, -0.0))
    """
    if not isinstance(v1, Vector):
        raise ValueError("The parameter v1 must be a Vector")

    # used in pbrt v4    
    if (method == "m2"):
        if v1.z > 0:sign = 1.
        else: sign =-1.
        term_1 = -1. / (sign + v1.z)
        term_2 = v1.x * v1.y * term_1
        v2 = Vector(1 + sign * (v1.x*v1.x) * term_1, sign * term_2, -sign * v1.x)
        v3 = Vector(term_2, sign + (v1.y*v1.y) * term_1, -v1.y)
    # used in pbrt v2 and v3
    elif (method == "m1"):
        if (abs(v1.x) > abs(v1.y)):
            invLen = 1/ math.sqrt(v1.x*v1.x + v1.z*v1.z)
            v2 = Vector(-v1.z*invLen, 0, v1.x*invLen)
        else:
            invLen = 1/ math.sqrt(v1.y*v1.y + v1.z*v1.z)
            v2 = Vector(0, v1.z*invLen, -v1.y*invLen)
        v3 = cross(v1, v2)
    else:
        raise ValueError("Only 2 choices for parameter method: 'm1' or 'm2'")
    
    return v2, v3


def distance(p1, p2):
    """
    Compute the distance between 2 points

    Parameters
    ----------
    p1 : Point
        The first point
    p2 : Point
        The second point

    Results
    -------
    out : float
        The distance between the 2 points
    
    Examples
    --------
    >>> p1 = gc.Point(0., 0., 0.)
    >>> p2 = gc.Point(0., 0., 10.)
    >>> gc.distance(p1,p2)
    10.0
    >>> p1 = gc.Point(1., 2., 1.9)
    >>> p2 = gc.Point(5., 15., 3.)
    >>> gc.distance(p1,p2)
    13.64587849865299
    """
    if isinstance(p1, Point) and isinstance(p2, Point):
        return (p1 - p2).length()
    else:
        raise ValueError('Only Point parameters are accepted')


def face_forward(a, b):
    """
    Flip the Vector/Normal a if the Vector/Normal b is in the opposite direction

    It can be useful to flip a surface normal so that it lies in the same
    hemisphere as a given vector.

    Parameters
    ----------
    a : Vector | Normal
        The Vector or Normal to potentially flip
    b : Vector | Normal
        The base Vector or Normal used for the flip

    Results
    -------
    out : Vector | Normal
        The potentially flipped Vector or Normal

    Examples
    --------
    >>> import geoclide as gc
    >>> n1 = gc.Normal(1., 0., 0.)
    >>> v1 = gc.Vector(-1., 0., 0.)
    >>> gc.face_forward(v1, n1)
    Vector(1.0, -0.0, -0.0)
    """
    if (isinstance(a, Vector) or isinstance(a, Normal)) and \
    (isinstance(b, Vector) or isinstance(b, Normal)):
        return (a*-1) if (dot(a, b) < 0) else a
    else:
        raise ValueError('Only Vector or Normal parameters are accepted')


def vmax(a):
    """
    Returns the largest component value of the Vector/Point/Normal

    Parameters
    ----------
    a : Vector | Point | Normal
        The vector/point/normal used
    
    Results
    -------
    out: float
        The largest vector/point/normal value
    
    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(2.,3.,1.)
    >>> gc.max(v1)
    3
    """
    if isinstance(a, Vector) or isinstance(a, Point) or isinstance(a, Normal):
        return int(np.max(a.to_numpy()))
    else:
        raise ValueError('Only a Vector, a Point or a Normal parameter is accepted')


def vmin(a):
    """
    Returns the smallest component value of the Vector/Point/Normal

    Parameters
    ----------
    a : Vector | Point | Normal
        The vector/point/normal used
    
    Results
    -------
    out: float
        The smallest vector/point/normal value
    
    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(2.,3.,1.)
    >>> gc.min(v1)
    1
    """
    if isinstance(a, Vector) or isinstance(a, Point) or isinstance(a, Normal):
        return int(np.min(a.to_numpy()))
    else:
        raise ValueError('Only a Vector, a Point or a Normal parameter is accepted')
    

def vargmax(a):
    """
    Returns the index of the Vector/Point/Normal component with the largest value

    Parameters
    ----------
    a : Vector | Point | Normal
        The vector/point/normal used
    
    Results
    -------
    out: int
        The index of the largest vector/point/normal value
    
    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(2.,3.,1.)
    >>> gc.argmax(v1)
    1
    """
    if isinstance(a, Vector) or isinstance(a, Point) or isinstance(a, Normal):
        return (0 if a.x>a.z else 2) if (a.x>a.y) else (1 if a.y>a.z else 2)
        #return int(np.argmax(a.to_numpy()))
    else:
        raise ValueError('Only a Vector, a Point or a Normal parameter is accepted')


def vargmin(a):
    """
    Returns the index of the Vector/Point/Normal component with the smallest value

    Parameters
    ----------
    a : Vector | Point | Normal
        The vector/point/normal used
    
    Results
    -------
    out: int
        The index of the smallest vector/point/normal value
    
    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(2.,3.,1.)
    >>> gc.argmin(v1)
    2
    """
    if isinstance(a, Vector) or isinstance(a, Point) or isinstance(a, Normal):
        return (0 if a.x<a.z else 2) if (a.x<a.y) else (1 if a.y<a.z else 2)
        #return int(np.argmin(a.to_numpy()))
    else:
        raise ValueError('Only a Vector, a Point or a Normal parameter is accepted')
    

def vabs(a):
    """
    Calculate the absolute value of each components of the vector/point/normal

    Parameters
    ----------
    a : Vector | Point | Normal
        The vector/point/normal used
    
    Results
    -------
    out: in progress...
    
    """
    if isinstance(a, Vector):
        return Vector(abs(a.x), abs(a.y), abs(a.z))
    elif isinstance(a, Point):
        return Point(abs(a.x), abs(a.y), abs(a.z))
    elif isinstance(a, Normal):
        return Normal(abs(a.x), abs(a.y), abs(a.z))
    else:
        raise ValueError('Only a Vector, a Point or a Normal parameter is accepted')


def permute(a, ix, iy=None, iz=None):
    """
    Permutes the vector/point/normal values according to the given indices

    Parameters
    ----------
    a : Vector | Point | Normal
    ix : int | np.ndarray
        The index of the value we want to keep as a remplacement for the x component.
        If ix is an np.ndarray -> the 1st component is ix and circumvent iy and iz parameters by the 2nd and 3th array components
    iy : int, optional
        The index of the value we want to keep as a remplacement for the y component.
    iz : int, optional
        The index of the value we want to keep as a remplacement for the z component.
    
    Results
    -------
    out : Vector | Point | Normal
        The vector/point/normal after the permute operation

    Examples
    --------
    >>> import geoclide as gc
    >>> v1 = gc.Vector(2., 3., 1.)
    >>> gc.permute(v1, 1, 0, 2)
    Vector(3.0, 2.0, 1.0)
    >>> gc.permute(v1, np.array([1, 0, 2]))
    Vector(3.0, 2.0, 1.0)
    """
    if isinstance(a, Vector) or isinstance(a, Point) or isinstance(a, Normal):
        if (isinstance(ix, np.ndarray)):
            if len(ix) != 3:
                raise ValueError("The size of the given array must be 3")
            if (  not ( (isinstance(ix[0], np.integer)) and
                       (isinstance(ix[1], np.integer)) and
                       (isinstance(ix[2], np.integer)) )  ):
                raise ValueError("The components of the given array must be integers")
            return Vector(a[ix[0]], a[ix[1]], a[ix[2]])
        elif( (isinstance(ix, int) or isinstance(ix, np.integer)) and
              (isinstance(iy, int) or isinstance(iy, np.integer)) and
              (isinstance(iz, int) or isinstance(iz, np.integer)) ):
            return Vector(a[ix], a[iy], a[iz])
        else:
            raise ValueError("Wrong parameter value(s) for ix and/or iy and/or iz")
    else:
        raise NameError('The parameter a must be a Vector or Point or Normal')