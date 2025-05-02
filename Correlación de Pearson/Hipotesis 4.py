import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar el dataset
df = pd.read_excel("correlacion_servidor.xlsx")

# Suponemos que las columnas son: 'Solicitudes' y 'Respuesta_ms'
x = df['Solicitudes_Concurrentes'].dropna()
y = df['Tiempo_Respuesta_ms'].dropna()

# 2. Gráfico de dispersión
plt.figure(figsize=(8, 6))
sns.scatterplot(x=x, y=y)
plt.title("Dispersión: Solicitudes_Concurrentes vs Tiempo_Respuesta")
plt.xlabel("Solicitudes_Concurrentes")
plt.ylabel("Tiempo_Respuesta_ms")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Correlación de Pearson (cola superior, positiva)
r, p_two_tailed = stats.pearsonr(x, y)
p_one_tailed = p_two_tailed / 2  # Para una cola (positiva)

print("Correlación de Pearson:")
print(f"r = {r:.4f}")
print(f"p (1 cola, H₁: ρ > 0) = {p_one_tailed:.4f}")

# 4. Interpretación
alpha = 0.05
print("\nInterpretación:")
if p_one_tailed < alpha and r > 0:
    print("Se rechaza H₀: Existe una correlación positiva significativa entre solicitudes y tiempo de respuesta.")
else:
    print("No se rechaza H₀: No hay evidencia suficiente de correlación positiva.")

# 5. Discusión sobre fuerza de la correlación
if abs(r) < 0.3:
    fuerza = "débil"
elif abs(r) < 0.6:
    fuerza = "moderada"
else:
    fuerza = "fuerte"

print(f"Fuerza de la correlación: {fuerza.capitalize()} (r = {r:.2f})")
