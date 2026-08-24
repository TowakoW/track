# import functions and packages
from horizons_api import fetch_horizons_data
from pprint import pprint
from astropy import units as u
from typing import Literal, Any


def horizons_specifics(naifids: list[int]) -> Any:
    """
    Organizes fetched data from NASA JPL's Horizons API, returns GM and ephemeris

    Parameters:
    -----
    "naifids": a list of one or more NAIF-IDs to object centers.

    All values returned in km/s

    Note: this function has undergone a LOT of different versions, ignore all commented lines please...
    """        
    # Allow a single int NAIF-ID or an iterable of NAIF-IDs
    if isinstance(naifids, int):
        naifids = [naifids]

    # Pulls ephimeris data from NASA JPL's Horizons API
    planet_data = []
    for naifid in naifids:
        # planet_data.append({"naifid": naifid, "data": fetch_horizons_data(naifid)})
        response = fetch_horizons_data(naifid)

    # if data_type == "gm":
        # Parse GM data for each id in NAIF-ID
    # for item in planet_data:
        raw = response["result"]
        lines = raw.splitlines()

        gm_line = next(
                (line for line in lines if "GM, km^3/s^2" in line or "GM (km^3/s^2)" in line or "GM (planet) km^3/s^2" in line),
                None,
            )
        gm = None
        if gm_line is not None:
                parts = gm_line.split("=")

                if len(parts) > 1:
                    gm_text = parts[1].split()[0]
                    gm_value = float(gm_text.split("+=")[0])
                    gm = gm_value * (u.km**3/u.s**2)

        # gm_val_km = None
        # if gm_value is not None:
        #         gm_val_km = float(gm_value) * (u.km**3 / u.s**2)
        #         item["gm"] = gm_val_km

            # # gm to (AU^3/s^2)
            # if gm_val_km is not None:
            #     gm_val_au = gm_val_km.to(u.au ** 3 / u.s ** 2)
            #     item["gm"] = gm_val_au
            # else:
            #     item["gm"] = None

        # print("NAIF-ID:", item["naifid"])
        # print("GM:", item["gm"] if gm_line is not None else "not found")
            # return item.get("gm")
        


    # Parse ephemeris data for each dictionary in NAIF-ID
    # if data_type == "ephemeris":
    # for item in planet_data:
            # raw = item["data"]["result"]
            # lines = raw.splitlines()

        start = lines.index("$$SOE") + 1
        end = lines.index("$$EOE")

        table_lines = [line for line in lines[start:end] if line.strip()]
        rows = [[value.strip() for value in line.split(",")]
        for line in table_lines]

            # Ephemeris data saved as a list udner "rows"
            # print("NAIF-ID:", item["naifid"])
            # print("--- EPHEMERIS LINES ---")
            # for num in rows:
                # print(num)
                # return(num)

    # if data_type == "all":
        # for item in planet_data:
        #     raw = item["data"]["result"]
        #     lines = raw.splitlines()
        #     rows = [line.split(",") for line in lines]

        #     print("NAIF-ID:", item["naifid"])
        #     for num in rows:
        #         print(num)
        
    # print("NAIF-ID:", item["naifid"])
    planet_data.append(
         {
              "naifid": naifid,
              "gm": gm,
              "ephemeris": rows,
         }
    )

    return planet_data
    

    

    # ALT: printing all output, comment out above for loop
    # print(lines)

# if __name__ == "__main__":
#     raise SystemExit(main())