import pandas as pd

url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/8a910e22264bc8011260f0aa9a093dcd/VIIRS_SNPP_NRT/world/1/2026-11-13"

df = pd.read_csv(url)

print(df.head())
print(df.columns)