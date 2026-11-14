
import pandas as pd
import mysql.connector

# =====================================
# 1. CONECTAR A MYSQL
# =====================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TU_PASSWORD",
    database="incendios_db"
)

cur = conn.cursor()

# =====================================
# 2. CREAR TABLA
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS Incendios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    latitud DECIMAL(6,2) NOT NULL,
    longitud DECIMAL(7,2) NOT NULL,
    incendio TINYINT NOT NULL,
    UNIQUE KEY observacion_unica
    (fecha, latitud, longitud)
)
""")

# =====================================
# 3. CARGAR CSV
# =====================================

df = pd.read_csv("incendios_0_1.csv")

print("Registros encontrados:", len(df))

# =====================================
# 4. INSERTAR DATOS
# =====================================

sql = """
INSERT INTO Incendios
(fecha, latitud, longitud, incendio)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
incendio = VALUES(incendio)
"""

datos = []

for _, row in df.iterrows():

    datos.append((
        pd.to_datetime(row["Fecha"]).date(),
        float(row["lat_celda"]),
        float(row["lon_celda"]),
        int(row["Incendio"])
    ))

# Insertar en bloques para ahorrar memoria
batch_size = 5000

for i in range(0, len(datos), batch_size):
    cur.executemany(sql, datos[i:i + batch_size])
    conn.commit()

# =====================================
# 5. CONSULTAR RESULTADOS
# =====================================

cur.execute("SELECT COUNT(*) FROM Incendios")

print("\nTotal de observaciones:", cur.fetchone()[0])

cur.execute("""
SELECT incendio, COUNT(*)
FROM Incendios
GROUP BY incendio
""")

print("\nDistribución de incendios:")

for row in cur.fetchall():
    print(row)

# =====================================
# 6. CERRAR CONEXIÓN
# =====================================

cur.close()
conn.close()

print("\nDatos guardados correctamente en MySQL.")
