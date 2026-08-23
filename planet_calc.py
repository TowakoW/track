# Calculating real time planet trajectory based on ephimeris data at time of call

# import
from astropy import constants as const
import numpy as np
from planet_data import System
import matplotlib.pyplot as plt
from datetime import datetime
# from planet_data import System
from typing import Literal
from planet_spherical import center_observer, cart_to_sph

# Constants:

# Needed Information:
# fetch_horizons_data(10) - Sun (GM)
# Target Planet position/velocity (x, y, z, vx, vy, vz)
# fetch_horizons_data(3) - earth barycenter data (x, y, z, vx, vy, vz)


# Physics Calc:
# F = G(m_1*m_2)/r**2
# a_planet = GM_sun/r**2


def plot(
        system: System,
        labels: list,
        colors: list,
        legend: bool,
        ax
    ) -> bool:
        """
        Plots the initial positions.
        Parameters:
        system: System
            system name ("solary_system")
        labels: list
            labels for objects
        colors: list
            list of colors used for objects
        legend: bool
            whether to show legend or not
        """

        # def quit_graph(event):
        #     """
        #     Conditions to manually quit the live-updating graph
        #     event == q to quit
        #     """
        #     nonlocal plotting
        #     if event.key =="q":
        #         plotting = False
        #         plt.close(fig)

        # Create figure and 3d axes

        # fig = ax.figure

        plt.ion()

        ax.clear()

        # Set graph size
        max_val = int(5.5e+09)

        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
        ax.set_zlim(-max_val, max_val)

        # count = 0
        # plot initial
        # plotting = True

        # Manual stop
        # fig.canvas.mpl_connect("key_press_event", quit_graph)

        # loop
        # while plotting:
        #     count += 1
        centered_positions = center_observer(system, labels)
        for i in range(system.num_particles):
            ax.scatter(
                    centered_positions[i, 0], centered_positions[i, 1], centered_positions[i, 2],
                    marker="o", color=colors[i],
                    # label=labels[i] if count == 1 else "_nolegend_"
                )
            # plt.pause(0.01)

            current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Set labels
            ax.set_xlabel("$x$ (KM)")
            ax.set_ylabel("$y$ (KM)")
            ax.set_zlabel("$z$ (KM)")
            ax.set_title(
                   f"Current Solar System Object Locations: {current_time}" 
                   )
            # fig.canvas.draw()
            # fig.canvas.flush_events()

            # # Stop live update after 30 seconds
            # if count > 30:
            #        plotting = False

        if legend:
               ax.legend()

        plt.ioff()
        # plt.show()
        # return plotting

        


# PHYSICS!!
# Semi-implicit Euler method

def acceleration(
                system: System,
                a: np.ndarray,
                ) -> None:
        """
        Computes the gravitational acceleration
        
        Parameters
        -----
        system: System
            System object ("solar_system")
        a: np.ndarray
            Gravitational acceleration array to be modified, shape (N, 3), (km/s^2)

        Equation
        -----
        a = sum(GM/r_norm^3 * r_ij)
        
        Reference
        -----
        "5 Steps to N-body Simulation" by alvinng4: 
        https://alvinng4.github.io/grav_sim/5_steps_to_n_body_simulation/step2/#implementation-3-advanced
        """

        # Empty acceleration array
        if a is None:
                a = np.zeros((system.num_particles, 3), dtype= float)
        a.fill(0.0)

        x = system.x
        GM = system.Gm

        # Displacement vector r
        r_ij = x[:, np.newaxis, :] - x[np.newaxis, :, :]

        # Normal r 
        r_norm = np.linalg.norm(r_ij, axis=2)

        # Compute 1/r^3
        with np.errstate(divide='ignore', invalid='ignore'):
                inv_r_cubed = 1.0/(r_norm ** 3)

        # Avoiding self-interaction, set diagonal elements to 0
        np.fill_diagonal(inv_r_cubed, 0.0)

        # Compute acceleration
        a[:] = np.sum(
                r_ij * inv_r_cubed[:, :, np.newaxis] * GM[:, np.newaxis, np.newaxis], axis=0
        )
        return a

def si_euler(system: System, dt: float, a: np.ndarray) -> np.ndarray:
        """
        Advance one step with semi-implicit Euler's method
        
        Parameters
        -----
        system: System
            system object ("solar_system"). 
        dt: float
            time step.
        a: np.ndarray
                Gravitational accelerations array with shape (N, 3), (km/s^2).
            """
        # acceleration(a, system)
        system.v += a * dt
        system.x += system.v * dt

        # return a
    