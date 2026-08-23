from planet_data import get_initial_conditions
from horizons_parse import horizons_specifics
import planet_calc
import numpy as np
from datetime import datetime
from planet_spherical import center_observer, cart_to_sph
from sky_map import sky_plot, sph_calc
import matplotlib.pyplot as plt
import base64
from pathlib import Path


INITIAL_CONDITIONS = "solar_system"

OUTPUT_INTERVAL = 1 # second(s)

def main() -> None:
    """Default units km, seconds"""

    def quit_graph(event):
            """
            Conditions to manually quit the live-updating graph
            event == q to quit
            """
            nonlocal continue_running
            if event.key =="q":
                continue_running = False
                plt.close(fig)

    # Initialize system
    print("Fetching data from NASA Horizons...")
    system, labels, colors, legend = get_initial_conditions(INITIAL_CONDITIONS)


    # Create acceleration array
    current_accel = np.zeros((system.num_particles, 3))

    # Physics simulation
    print("Starting physics engine...")

    while True:
        # Record loop start time
        loop_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(loop_start_time)

        # -----Data Output-----

        print("Number of Objects:\n", system.num_particles)
        print("Initial Positions (km):\n", system.x)
        print("Initial Velocities (km/s):\n", system.v)
        print("Object GM (km^3/s^2):\n", system.Gm)


        # ----Plots-----
        fig = plt.figure(figsize = (14, 7))
        cartesian_ax = fig.add_subplot(1, 2, 1, projection='3d')
        polar_ax = fig.add_subplot(1, 2, 2, projection='polar')

        fig.canvas.mpl_connect("key_press_event", quit_graph)

        #-----Polar Projection-----
        alt_az = sph_calc(system, labels)

        sky_plot(system, 
                 labels, 
                 colors, 
                 legend, 
                 alt_az,
                 polar_ax
                 )

        #-----Cartesian Projection (LIVE)-----
        continue_running = True
        
        while continue_running:
            # -----PHYSICS!!!-----
            current_accel = planet_calc.acceleration(system, current_accel)
            planet_calc.si_euler(system, OUTPUT_INTERVAL, current_accel)
        
            # -----Update coords-----
            planet_calc.plot(
            system,
            labels,
            colors,
            legend, 
            cartesian_ax,
            )

            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            plt.pause(0.01)

        if not continue_running:
            break




if __name__ == "__main__":
    main()