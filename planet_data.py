import numpy as np
from typing import Tuple, List, Optional
from horizons_parse import horizons_specifics
from datetime import datetime

'''
references:
https://alvinng4.github.io/grav_sim/5_steps_to_n_body_simulation/step1/
'''


class System:
    def __init__(self, num_particles: int | None = None, Gm: np.ndarray | None = None, m: np.ndarray | None = None, x: np.ndarray | None = None, v: np.ndarray | None = None) -> None:
        # Prefer to infer number of particles from provided position array
        if x is not None:
            self.num_particles = int(len(x))
        else:
            self.num_particles = int(num_particles) if num_particles is not None else 0

        # Store gravitational parameters and masses
        # keep attribute name `Gm` to match callers
        self.Gm = Gm
        # default masses to ones if not provided
        self.m = m if m is not None else (np.ones(self.num_particles) if self.num_particles > 0 else None)
        self.x = x
        self.v = v

    def center_of_mass_correction(self) -> None:
        """ Set center of mass of position and velocity to zero"""
        if self.x is None or self.v is None or self.m is None:
            return

        x_cm = np.zeros(3)
        v_cm = np.zeros(3)
        M = 0.0
        for i in range(self.num_particles):
            x_cm += self.m[i] * self.x[i]
            v_cm += self.m[i] * self.v[i]
            M += self.m[i]
        if M == 0:
            return
        x_cm /= M
        v_cm /= M
        self.x -= x_cm
        self.v -= v_cm




def get_initial_conditions(initial_condition: dict
                           ) -> Tuple[System, List[Optional[str]]]:
        """
        Returns initial conditions for objects in 
        Solar System in km and seconds:
            Num_particles
            Gm (mass * G constant) (km^3/s^2)
            x (position) (km)
            v (velocity) (km/s)
        
        
        Parameters
        -----
        initial_condition: str
            name for initial condition
            "solar_system" for solar system data
        
        Returns
        -----
        system: System
            name of system
        labels: list
            Lables for objects
        colors: list
            colors for objects
        legend: bool
            whether to show legend
        """

        # GM values (AU^3/s^2)
        sun_data = horizons_specifics(10),
        mercury_data = horizons_specifics(199),
        venus_data = horizons_specifics(299),
        earth_data = horizons_specifics(399),
        mars_data = horizons_specifics(499),
        jupiter_data = horizons_specifics(599),
        saturn_data = horizons_specifics(699),
        uranus_data = horizons_specifics(799),
        neptune_data = horizons_specifics(899),
        pluto_data = horizons_specifics(999)
        moon_data = horizons_specifics(301),
        phobos_data = horizons_specifics(401),
        deimos_data = horizons_specifics(402),
        io_data = horizons_specifics(501),
        europa_data = horizons_specifics(502),
        ganymede_data = horizons_specifics(503)


        # GM data:
        GM_AU_S = {
                "Sun": sun_data['gm'],
                "Mercury": mercury_data['gm'],
                "Venus": venus_data['gm'],
                "Earth": earth_data['gm'],
                "Mars": mars_data['gm'],
                "Jupiter": jupiter_data['gm'],
                "Saturn": saturn_data['gm'],
                "Uranus": uranus_data['gm'],
                "Neptune": neptune_data['gm'],
                "Pluto": pluto_data['gm'],
                "Moon": moon_data['gm'],
                "Phobos": phobos_data['gm'],
                "Deimos": deimos_data['gm'],
                'Io': io_data['gm'],
                "Europa": europa_data['gm'],
                "Ganymede": ganymede_data['gm']
        }

        # Ephemeris data:
        sun_eph = sun_data['ephemeris']
        mercery_eph = mercury_data['ephemeris']
        venus_eph = venus_data['ephemeris']
        earth_eph = earth_data['ephemeris']
        mars_eph = mars_data['ephemeris']
        jupiter_eph = jupiter_data['ephemeris']
        saturn_eph = saturn_data['ephemeris']
        uranus_eph =  uranus_data['gm']
        neptune_eph = neptune_data['ephemeris']
        pluto_eph = pluto_data['ephemeris']
        moon_eph = moon_data['ephemeris']
        phobos_eph = phobos_data['ephemeris']
        deimos_eph = deimos_data['ephemeris']
        io_eph = io_data['ephemeris']
        europa_eph = europa_data['ephemeris']
        ganymede_eph = ganymede_data['ephemeris']


        # ephemeris rows: [jd, datetime, x, y, z, vx, vy, vz, ...]
        SOLAR_SYSTEM_POS = {
            "Sun": sun_eph[2:5],
            "Mercury": mercery_eph[2:5],
            "Venus": venus_eph[2:5],
            "Earth": earth_eph[2:5],
            "Mars": mars_eph[2:5],
            "Jupiter": jupiter_eph[2:5],
            "Saturn": saturn_eph[2:5],
            "Uranus": uranus_eph[2:5],
            "Neptune": neptune_eph[2:5],
            "Pluto": pluto_eph[2:5],
            "Moon": moon_eph[2:5],
            "Phobos": phobos_eph[2:5],
            "Deimos": deimos_eph[2:5],
            "Io": io_eph[2:5],
            "Europa": europa_eph[2:5],
            "Ganymede": ganymede_eph[2:5]
        }

        SOLAR_SYSTEM_VEL = {
            "Sun": sun_eph[5:8],
            "Mercury": mercery_eph[5:8],
            "Venus": venus_eph[5:8],
            "Earth": earth_eph[5:8],
            "Mars": mars_eph[5:8],
            "Jupiter": jupiter_eph[5:8],
            "Saturn": saturn_eph[5:8],
            "Uranus": uranus_eph[5:8],
            "Neptune": neptune_eph[5:8],
            "Pluto": pluto_eph[5:8],
            "Moon": moon_eph[5:8],
            "Phobos": phobos_eph[5:8],
            "Deimos": deimos_eph[5:8],
            "Io": io_eph[5:8],
            "Europa": europa_eph[5:8],
            "Ganymede": ganymede_eph[5:8]
            }

        SOLAR_SYSTEM_COLORS = {
                "Sun": 'gold',
                "Mecury": 'tomato',
                "Venus": 'burlywood',
                "Earth": 'lightseagreen',
                "Mars": 'orangered',
                "Jupiiter": 'peru',
                "Saturn": 'slategrey',
                "Uranus": 'olive',
                "Neptune": 'teal',
                "Pluto": 'aquamarine',
                "Moon": 'grey',
                "Phobos": 'tan',
                "Deimos": 'cornflowerblue',
                "Io": 'lawngreen',
                "Europa": 'pink',
                "Ganymede": 'brown'



        }


        if initial_condition == "solar_system":
        # m = np.array(
        #     [
        #         SOLAR_SYSTEM_MASSES["Sun"],
        #         SOLAR_SYSTEM_MASSES["Mercury"],
        #         SOLAR_SYSTEM_MASSES["Venus"],
        #         SOLAR_SYSTEM_MASSES["Earth"],
        #         SOLAR_SYSTEM_MASSES["Mars"],
        #         SOLAR_SYSTEM_MASSES["Jupiter"],
        #         SOLAR_SYSTEM_MASSES["Saturn"],
        #         SOLAR_SYSTEM_MASSES["Uranus"],
        #         SOLAR_SYSTEM_MASSES["Neptune"],
        #     ]
        # )

            G1 = np.array(GM_AU_S["Sun"])
            G2 = np.array(GM_AU_S["Mercury"])
            G3 = np.array(GM_AU_S["Venus"])
            G4 = np.array(GM_AU_S["Earth"])
            G5 = np.array(GM_AU_S["Mars"])
            G6 = np.array(GM_AU_S["Jupiter"])
            G7 = np.array(GM_AU_S["Saturn"])
            G8 = np.array(GM_AU_S["Uranus"])
            G9 = np.array(GM_AU_S["Neptune"])
            G10 = np.array(GM_AU_S["Pluto"])
            G11 = np.array(GM_AU_S["Moon"])
            G12 = np.array(GM_AU_S["Phobos"])
            G13 = np.array(GM_AU_S["Deimos"])
            G14 = np.array(GM_AU_S['Io'])
            G15 = np.array(GM_AU_S["Europa"])
            G16 = np.array(GM_AU_S['Ganymede'])
            
            R1 = np.array(SOLAR_SYSTEM_POS["Sun"], dtype=float)
            R2 = np.array(SOLAR_SYSTEM_POS["Mercury"], dtype=float)
            R3 = np.array(SOLAR_SYSTEM_POS["Venus"], dtype=float)
            R4 = np.array(SOLAR_SYSTEM_POS["Earth"], dtype=float)
            R5 = np.array(SOLAR_SYSTEM_POS["Mars"], dtype=float)
            R6 = np.array(SOLAR_SYSTEM_POS["Jupiter"], dtype=float)
            R7 = np.array(SOLAR_SYSTEM_POS["Saturn"], dtype=float)
            R8 = np.array(SOLAR_SYSTEM_POS["Uranus"], dtype=float)
            R9 = np.array(SOLAR_SYSTEM_POS["Neptune"], dtype=float)
            R10 = np.array(SOLAR_SYSTEM_POS["Pluto"], dtype=float)
            R11 = np.array(SOLAR_SYSTEM_POS["Moon"], dtype=float)
            R12 = np.array(SOLAR_SYSTEM_POS["Phobos"], dtype=float)
            R13 = np.array(SOLAR_SYSTEM_POS["Deimos"], dtype=float)
            R14 = np.array(SOLAR_SYSTEM_POS["Io"], dtype=float)
            R15 = np.array(SOLAR_SYSTEM_POS["Europa"], dtype=float)
            R16 = np.array(SOLAR_SYSTEM_POS["Ganymede"], dtype=float)



            V1 = np.array(SOLAR_SYSTEM_VEL["Sun"], dtype=float)
            V2 = np.array(SOLAR_SYSTEM_VEL["Mercury"], dtype=float)
            V3 = np.array(SOLAR_SYSTEM_VEL["Venus"], dtype=float)
            V4 = np.array(SOLAR_SYSTEM_VEL["Earth"], dtype=float)
            V5 = np.array(SOLAR_SYSTEM_VEL["Mars"], dtype=float)
            V6 = np.array(SOLAR_SYSTEM_VEL["Jupiter"], dtype=float)
            V7 = np.array(SOLAR_SYSTEM_VEL["Saturn"], dtype=float)
            V8 = np.array(SOLAR_SYSTEM_VEL["Uranus"], dtype=float)
            V9 = np.array(SOLAR_SYSTEM_VEL["Neptune"], dtype=float)
            V10 = np.array(SOLAR_SYSTEM_VEL["Pluto"], dtype=float)
            V11 = np.array(SOLAR_SYSTEM_VEL["Moon"], dtype=float)
            V12 = np.array(SOLAR_SYSTEM_VEL["Phobos"], dtype=float)
            V13 = np.array(SOLAR_SYSTEM_VEL["Deimos"], dtype=float)
            V14 = np.array(SOLAR_SYSTEM_VEL["Io"], dtype=float)
            V15 = np.array(SOLAR_SYSTEM_VEL["Europa"], dtype=float)
            V16 = np.array(SOLAR_SYSTEM_VEL["Ganymede"], dtype=float)


            Gm = np.array(
                   [
                         G1,
                         G2,
                         G3,
                         G4,
                         G5,
                         G6,
                         G7,
                         G8,
                         G9,
                         G10,
                         G11,
                         G12,
                         G13,
                         G14,
                         G15,
                         G16
                   ]
            )

            x = np.array(
                    [  
                        R1,
                        R2,
                        R3,
                        R4,
                        R5,
                        R6,
                        R7,
                        R8,
                        R9,
                        R10,
                        R11,
                        R12,
                        R13,
                        R14,
                        R15,
                        R16
                    ]
                )
            v = np.array(
                    [
                        V1,
                        V2,
                        V3,
                        V4,
                        V5,
                        V6,
                        V7,
                        V8,
                        V9,
                        V10,
                        V11,
                        V12,
                        V13,
                        V14,
                        V15,
                        V16
                    ]
                )

            system = System(
                num_particles= 16,
                Gm=Gm,
                x=x,
                v=v,
                # m=m,
                # G=G,
                )
            system.center_of_mass_correction()

            labels = list(SOLAR_SYSTEM_POS.keys())
            colors = list(SOLAR_SYSTEM_COLORS.values())
            legend = True

            return system, labels, colors, legend

        else:
            raise ValueError(f"Initial condition not recognized: {initial_condition}.")