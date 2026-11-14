
import pandas as pd
import numpy as np

# =====================================
# 1. DESCARGAR DATOS DE NASA FIRMS
# =====================================

MAP_KEY = "8a910e22264bc8011260f0aa9a093dcd"

url = (
    f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    f"{MAP_KEY}/VIIRS_NOAA21_NRT/"
    f"world/3"
)

print("Descargando datos de NASA FIRMS...")

df = pd.read_csv(url)

if df.empty:
    print("No se encontraron detecciones.")
    exit()

print("Incendios detectados:", len(df))

# =====================================
# 2. PROCESAR FECHAS Y COORDENADAS
# =====================================

df["acq_date"] = pd.to_datetime(df["acq_date"])

tamano_celda = 0.1

df["lat_celda"] = (
    np.floor(df["latitude"] / tamano_celda) * tamano_celda
)

df["lon_celda"] = (
    np.floor(df["longitude"] / tamano_celda) * tamano_celda
)

# Cada detección representa un positivo
incendios = df[
    ["acq_date", "lat_celda", "lon_celda"]
].drop_duplicates()

incendios = incendios.rename(
    columns={"acq_date": "Fecha"}
)

# =====================================
# 3. CREAR TODAS LAS COMBINACIONES
# =====================================

fechas = pd.date_range(
    start=df["acq_date"].min(),
    end=df["acq_date"].max(),
    freq="D"
)

latitudes = np.round(
    np.arange(14.5, 32.7, tamano_celda), 2
)

longitudes = np.round(
    np.arange(-118.4, -86.7, tamano_celda), 2
)

completo = pd.MultiIndex.from_product(
    [fechas, latitudes, longitudes],
    names=["Fecha", "lat_celda", "lon_celda"]
).to_frame(index=False)

# =====================================
# 4. IDENTIFICAR INCENDIOS
# =====================================

completo = completo.merge(
    incendios,
    on=["Fecha", "lat_celda", "lon_celda"],
    how="left",
    indicator=True
)

completo["Incendio"] = np.where(
    completo["_merge"] == "both", 1, 0
)

completo = completo.drop(columns=["_merge"])

# =====================================
# 5. GUARDAR ARCHIVO CSV
# =====================================

completo.to_csv(
    "incendios_0_1.csv",
    index=False
)

# =====================================
# 6. MOSTRAR RESULTADOS
# =====================================

print("\nArchivo creado: incendios_0_1.csv")

print("\nPrimeros registros:")
print(completo.head(10))

print("\nCantidad de observaciones:")
print(len(completo))

print("\nDistribución de resultados:")
print(completo["Incendio"].value_counts())

print("\nPorcentajes:")
print(
    (completo["Incendio"].value_counts(normalize=True) * 100)
    .round(2)
)
