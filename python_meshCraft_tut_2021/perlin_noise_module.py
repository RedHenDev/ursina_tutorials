"""Perlin Noise calculating lib.
Includes each_with_each, hasher and RandVec
so that all part of a single file.
"""
import math
import random
from collections import Iterable
from typing import Optional, Union

#from rand_vec import RandVec
#from tools import each_with_each, hasher

from typing import List, Tuple

#from tools import dot, fade, product, sample_vector

"""File for placing functions used in library."""

import math
import random
from typing import Generator, List, Tuple, Union


def dot(
    vec1: Union[List, Tuple],
    vec2: Union[List, Tuple],
) -> Union[float, int]:
    """Two vectors dot product.

    Parameters:
        vec1: List[float] - first vector
        vec2: List[float] - second vector

    Returns:
        Dot product of 2 vectors

    Raises:
        ValueError: if length not equal
    """
    if len(vec1) != len(vec2):
        raise ValueError('lengths of two vectors are not equal')
    return sum([val1 * val2 for val1, val2 in zip(vec1, vec2)])


def sample_vector(dimensions: int, seed: int) -> List[float]:
    """Sample normalized vector given length.

    Parameters:
        dimensions: int - space size
        seed: Optional[int] - random seed value

    Returns:
        List[float] - normalized random vector of given size
    """
    st = random.getstate()
    random.seed(seed)

    vec = []
    for _ in range(dimensions):
        vec.append(random.uniform(-1, 1))  # noqa: S311

    random.setstate(st)
    return vec


def fade(given_value: float) -> float:
    """Smoothing [0, 1] values.

    Parameters:
        given_value: float [0, 1] value for smoothing

    Returns:
        smoothed [0, 1] value

    Raises:
        ValueError: if input not in [0, 1]
    """
    if given_value < 0 or given_value > 1:
        raise ValueError('expected to have value in [0, 1]')
    return 6 * math.pow(given_value, 5) - 15 * math.pow(given_value, 4) + 10 * math.pow(given_value, 3)  # noqa: WPS221, WPS432, E501


def hasher(coors: Tuple[int]) -> int:
    """Hashes coordinates to integer number and use obtained number as seed.

    Parameters:
        coors: List[int] - array of coordinates

    Returns:
        hash of coordinates in integer
    """
    return max(
        1,
        int(abs(
            dot(
                [10 ** coordinate for coordinate in range(len(coors))],
                coors,
                ) + 1,
        )),
    )


def product(iterable: Union[List, Tuple]) -> float:
    """Multiplies values of iterable  each with each.

    Parameters:
        iterable: - any iterable

    Returns:
        product of values
    """
    if len(iterable) == 1:
        return iterable[0]
    return iterable[0] * product(iterable[1:])


def each_with_each(
    arrays: List[Tuple[int, int]],
    prev=(),
) -> Generator[Tuple[int], None, None]:
    """Create iterable for given array of arrays.

    Each value connected in array with with each value from other arrays

    Parameters:
        arrays: list of lists to make mixing
        prev: value accumulating values from previous arrays

    Yields:
        generator with elements
    """
    for el in arrays[0]:
        new = prev + (el,)
        if len(arrays) == 1:
            yield new
        else:
            yield from each_with_each(arrays[1:], prev=new)


class RandVec(object):
    """Vectors to give weights and contribute in final value."""

    def __init__(self, coordinates: Tuple[int], seed: int):
        """Vector initializer in specified coordinates.

        Parameters:
            coordinates: Tuple[int] - vector coordinates
            seed: int - random init seed
        """
        self.coordinates = coordinates
        self.vec = sample_vector(dimensions=len(self.coordinates), seed=seed)

    def dists_to(self, coordinates: List[float]) -> Tuple[float, ...]:
        """Calculate distance to given coordinates.

        Parameters:
            coordinates: Tuplie[int] - coordinates to calculate distance

        Returns:
            distance

        """
        return tuple(
            coor1 - coor2
            for coor1, coor2 in zip(coordinates, self.coordinates)
            )

    def weight_to(self, coordinates: List[float]) -> float:
        """Calculate this vector weights to given coordinates.

        Parameters:
            coordinates: Tuple[int] - target coordinates

        Returns:
            weight
        """
        weighted_dists = list(
            map(
                lambda dist: fade(1-abs(dist)),
                self.dists_to(coordinates),
            ))

        return product(weighted_dists)

    def get_weighted_val(self, coordinates: List[float]) -> float:
        """Calculate weighted contribution of this vec to final result.

        Parameters:
            coordinates: calculate weighted relative to this coordinates

        Returns:
            weighted contribution
        """
        return self.weight_to(coordinates) * dot(
            self.vec, self.dists_to(coordinates),
            )

class PerlinNoise(object):
    """Smooth random noise generator.

    read more https://en.wikipedia.org/wiki/Perlin_noise
    """

    def __init__(self, octaves: float = 1, seed: Optional[int] = None):
        """Perlin Noise object initialization class.

            ex.: noise = PerlinNoise(n_dims=2, octaves=3.5, seed=777)

        Parameters:
            octaves : optional positive float, default = 1
                positive number of sub rectangles in each [0, 1] range
            seed : optional positive int, default = None
                specified seed

        Raises:
            ValueError: if seed is negative
        """
        if octaves <= 0:
            raise ValueError('octaves expected to be positive number')

        if seed is not None and not isinstance(seed, int) and seed <= 0:
            raise ValueError('seed expected to be positive integer number')

        self.octaves: float = octaves
        self.seed: int = seed if seed else random.randint(1, 10 ^ 5)  # noqa: S311, E501

    def __call__(self, coordinates: Union[int, float, Iterable]) -> float:
        """Forward request to noise function.

        Parameters:
            coordinates: float or list of coordinates

        Returns:
            noise_value
        """
        return self.noise(coordinates)

    def noise(self, coordinates: Union[int, float, Iterable]) -> float:
        """Get perlin noise value for given coordinates.

        Parameters:
            coordinates: float or list of coordinates

        Returns:
            noise_value

        Raises:
            TypeError: if coordinates is not valid type
        """
        if not isinstance(coordinates, (int, float, Iterable)):
            raise TypeError('coordinates must be int, float or iterable')

        if isinstance(coordinates, (int, float)):
            coordinates = [coordinates]

        coordinates = list(
            map(lambda coordinate: coordinate * self.octaves, coordinates),
        )

        coor_bounding_box = [
            (math.floor(coordinate), math.floor(coordinate+1))
            for coordinate in coordinates
        ]
        return sum([
            RandVec(
                coors, self.seed * hasher(coors),
            ).get_weighted_val(coordinates)
            for coors in each_with_each(coor_bounding_box)
        ])
