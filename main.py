from planet_data import get_initial_conditions
from horizons_parse import horizons_specifics
import planet_calc
import numpy as np
from datetime import datetime
from planet_spherical import center_observer, cart_to_sph


INITIAL_CONDITIONS = "solar_system"

OUTPUT_INTERVAL = 1 # second(s)

def main() -> None:
    """Default units km, seconds"""

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

        # -----PHYSICS!!!-----
        current_accel = planet_calc.acceleration(system, current_accel)
        planet_calc.si_euler(system, OUTPUT_INTERVAL, current_accel)

        # -----Data Output-----

        print("Number of Objects:\n", system.num_particles)
        print("Initial Positions (km):\n", system.x)
        print("Initial Velocities (km/s):\n", system.v)
        print("Object GM (km^3/s^2):\n", system.Gm)

        continue_running = planet_calc.plot(
            system=system,
            labels=labels,
            colors=colors,
            legend=legend
            )
        if not continue_running:
            break



if __name__ == "__main__":
    main()