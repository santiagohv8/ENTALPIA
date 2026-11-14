import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("datos.csv")

X = df[["Temperatura", "Humedad", "Viento"]]
Y = df["Incendio"]

X = sm.add_constant(X)

modelo = sm.Logit(Y, X)
resultado = modelo.fit()

print(resultado.summary())
print(resultado.params)