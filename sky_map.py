# Generating skymap based on coordinates


# imports
from planet_spherical import cart_to_sph, alt_azmuth, find_RA_DEC
import numpy as np
from planet_data import System
import matplotlib.pyplot as plt
from datetime import datetime

def sph_calc(
        system: System,
        labels: list,
):
    spherical_positions = find_RA_DEC(system, labels)

    # get altitude and azimuth
    alt_az_positions = []
    for radius, ra, dec in spherical_positions:
        altitude, azimuth = alt_azmuth(ra, dec)
        alt_az_positions.append([altitude, azimuth])

    return np.array(alt_az_positions)

def sky_plot(
        system: System,
        labels: list,
        colors: list,
        legend: bool,
        alt_az,
        ax):
    """
    Plot polar graph scatterplot showing locations where objects can be found for night sky
    """

    # fig = plt.figure(figsize=(7, 7))
    # ax = fig.add_subplot(111, projection='polar')

    ax.clear()

    # match astronomical conventions
    ax.set_theta_zero_location('N') # put 0 degrees (north) at top
    ax.set_theta_direction(-1) # make angles increase clockwise

    # altitude to radial dist from center
    ax.set_rmax(90)
    ax.set_rmin(0)

    # replace radial labels w altitude markings
    ax.set_rticks([0, 30, 60, 90])
    ax.set_yticklabels(['90°', '60°', '30°', '0° (horizon)'])

    # compass label appearance
    ax.set_xticks(np.arange(8) * (np.pi / 4))
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

    # loop and plot visible planets
    visible_labels = [label for label in labels if label != "Earth"]
    visible_colors = [color for label, color in zip(labels, colors) if label != "Earth"]
    for index, alt_az in enumerate(alt_az):
        name = visible_labels[index]
        alt_rad, az_rad = alt_az[0], alt_az[1]

        alt_deg = np.degrees(alt_rad)

        # Filter only obj above horizon line
        if alt_deg < 0:
            print(f"Skipping {name}: Hidden below horizon (ALT: {alt_deg:.1f}°)")
            continue

        r_plot = 90.0 - alt_deg

        ax.scatter(az_rad, r_plot, c=visible_colors[index], s=100, label=name, zorder=3)

    if legend == True:
        ax.legend(loc='upper left')

    theta = np.linspace(0, 2 * np.pi, 360)
    ax.plot(theta, np.full_like(theta, 90), color="black", linewidth=1)

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ax.set_title(
        f"Local Sky View (Topocentric Polar Projection)\nTime: {time}",
        pad=18,
        fontsize=10,
    )
    plt.grid(True, linestyle='--', alpha=0.6)
    ax.figure.tight_layout()
    # plt.show()



if __name__ == "__main__":
    sky_plot()

