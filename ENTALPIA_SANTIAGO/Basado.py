
import pandas as pd
import sqlite3

# =====================================
# 1. CONECTAR A SQLITE
# =====================================

conn = sqlite3.connect("incendios.sqlite")
cur = conn.cursor()

# =====================================
# 2. CREAR TABLA
# =====================================

cur.executescript("""
DROP TABLE IF EXISTS Incendios;

CREATE TABLE Incendios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    latitud REAL,
    longitud REAL,
    incendio INTEGER
);
""")

# =====================================
# 3. CARGAR CSV
# =====================================

df = pd.read_csv("incendios_0_1.csv")

print("Registros encontrados:", len(df))

# =====================================
# 4. INSERTAR DATOS EN SQLITE
# =====================================

datos = []

for _, row in df.iterrows():

    datos.append((
        row["Fecha"],
        row["lat_celda"],
        row["lon_celda"],
        int(row["Incendio"])
    ))

cur.executemany("""
    INSERT INTO Incendios
    (fecha, latitud, longitud, incendio)
    VALUES (?, ?, ?, ?)
""", datos)

conn.commit()

# =====================================
# 5. MOSTRAR RESULTADOS
# =====================================

print("\nDatos guardados correctamente.")

cur.execute("SELECT COUNT(*) FROM Incendios")
print("Total de observaciones:", cur.fetchone()[0])

cur.execute("""
    SELECT incendio, COUNT(*)
    FROM Incendios
    GROUP BY incendio
""")

print("\nDistribución de incendios:")

for row in cur.fetchall():
    print(row)

# =====================================
# 6. CERRAR CONEXION
# =====================================

conn.close()
