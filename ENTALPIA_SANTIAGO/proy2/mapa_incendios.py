
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# =====================================
# 1. CARGAR DATOS
# =====================================

df = pd.read_csv("incendios_modelo.csv")

df = df.dropna(subset=["latitude", "longitude", "Incendio"])

# =====================================
# 2. CREAR MAPA
# =====================================

centro = [
    df["latitude"].mean(),
    df["longitude"].mean()
]

mapa = folium.Map(
    location=centro,
    zoom_start=5,
    tiles="OpenStreetMap"
)

# Agrupar marcadores para mejorar el rendimiento
marcadores = MarkerCluster().add_to(mapa)

# =====================================
# 3. AGREGAR DETECCIONES
# =====================================

for _, fila in df.iterrows():

    if int(fila["Incendio"]) == 1:
        color = "green"
        confianza = "Nominal o alta"
    else:
        color = "red"
        confianza = "Baja"

    popup = f"""
    <b>Clasificación:</b> {confianza}<br>
    <b>Latitud:</b> {fila['latitude']:.2f}<br>
    <b>Longitud:</b> {fila['longitude']:.2f}<br>
    <b>Temperatura TI4:</b> {fila['bright_ti4']:.2f}<br>
    <b>Temperatura TI5:</b> {fila['bright_ti5']:.2f}<br>
    <b>FRP:</b> {fila['frp']:.2f}
    """

    folium.CircleMarker(
        location=[
            fila["latitude"],
            fila["longitude"]
        ],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.75,
        popup=folium.Popup(popup, max_width=250)
    ).add_to(marcadores)

# =====================================
# 4. GUARDAR MAPA
# =====================================

mapa.save("mapa_incendios.html")

print("Mapa generado: mapa_incendios.html")
