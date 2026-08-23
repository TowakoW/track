# Converting from cartesian coordinates (x,y,z) to spherical (right ascension, declination, r)

# import
from astropy import constants as const
import numpy as np
from planet_data import System
import matplotlib.pyplot as plt
from datetime import datetime
# from planet_spherical import cart_to_sph, center_observer
from steal_data import find_LST, fetch_coords
import math
# from planet_data import System
# from typing import Literal


def cart_to_sph(position: np.ndarray) -> np.ndarray:
    """
    Converting cartesian coordinates to RA/DEC from the perspective of a location on Earth

    Parameters
    -----
    position: np.ndarray
        One Cartesian position in the form [x, y, z].
    
    Equations
    -----
    r = sqrt(x**2 + y**2 + z**2)

    dec = arcsin(z/r)

    asc = atan2(y, x)
    """
    # Defining x, y, and z from the position vector:
    x_pos, y_pos, z_pos = position
    
   # conversions
    r = np.sqrt(x_pos**2 + y_pos**2 + z_pos**2)
    dec = np.arcsin(z_pos/r)
    asc = np.atan2(y_pos, x_pos)
    return np.array([r, asc, dec])


def center_observer(system: System, labels):
    """
    Converts system center to a point on Earth (topocentric coordinates). 

    Parameters
    -----
    system: System
        system object ("solar_system")
    location: str
        latitude/longitude/LST coordinates on the Earth to be the obervation site
    """
    # Defining x, y, and z within system.x for convenience:
    # x_pos = system.x[0]
    # y_pos = system.x[1]
    # z_pos = system.x[2]

    earth_index = labels.index("Earth")
    earth_pos = system.x[earth_index]

    earth_center_pos = system.x - earth_pos

    return earth_center_pos

def alt_azmuth(ra, dec):
    """
    Calculate hour angle, altitude, and azimuth using spherical coordinates
    
    Parameters
    -----
    ra: float
        right ascension, radians
    dec: float
        declination, radians

    
    Equations
    -----
    Hour angle (H) = LST - RA
        radians (where H >= 0)

    altitude (a) = arcsin(sin(dec)sin(lat) + cos(dec)cos(lat)cos(H))

    azimuth (A) = arccos((sin(dec)-sin(a)sin(lat))/cos(a)cos(lat))
    """
    coordinates = fetch_coords()
    LST = find_LST(coordinates)
    LST_rad = LST * (np.pi/180)

    lat = coordinates[0]
    # lon = coordinates[1]
    # latitude radians
    lat_rad = lat * (math.pi/180)

    # calculate hour angle (rad)
    H = LST_rad - ra
    # normalize
    H_norm = normalize(H)


    # calculate altitude
    alt_ins = (np.sin(dec) * np.sin(lat_rad)) + (np.cos(dec) * np.cos(lat_rad) * np.cos(H_norm))
    altitude = np.arcsin(alt_ins)

    # calculate azimuth
    y = -np.cos(dec) * np.sin(H_norm)
    x = np.sin(dec) * np.cos(lat_rad) - np.cos(dec) * np.sin(lat_rad) * np.cos(H_norm)
    azimuth = np.arctan2(y, x) 
    azimuth_norm = azimuth % (2 * np.pi)

    print(altitude, azimuth_norm)
    return np.array([altitude, azimuth_norm])

def normalize(val):
    """
    normalize value between -pi and pi
    
    to be used for hour angle
    """
    norm = val - 2 * np.pi * math.floor((val + np.pi)/(2 * np.pi))
    return norm

def find_RA_DEC(system, labels):
    """
    Finds topocentric RA and DEC, for use in alt_azmuth() function
    Returns an array of (r, ra, dec)
    
    Parameters
    -----
    system: System
        system object
    labels: list
        system labels
    """
    centered_positions = center_observer(system, labels)
    positions = []

    for index, label in enumerate(labels):
        if label == "Earth":
            continue

        planet_position = centered_positions[index]
        spherical_coords = cart_to_sph(planet_position)
        positions.append( spherical_coords)
    return positions