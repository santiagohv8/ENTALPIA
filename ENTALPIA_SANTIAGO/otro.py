import pandas as pd

MAP_KEY = "8a910e22264bc8011260f0aa9a093dcd"

url = (
    f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    f"{MAP_KEY}/VIIRS_NOAA21_NRT/"
    f"world/1"
    #-118.4,14.5,-86.7,32.7
)

df = pd.read_csv(url)

print("Cantidad de incendios:", len(df))

if len(df) > 0:
    df.to_csv("incendios.csv", index=False)
    print("Datos guardados en incendios.csv")
    print(df.head())
else:
    print("No se encontraron incendios.")