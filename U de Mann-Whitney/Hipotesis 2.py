import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 1. Cargar los datos
df = pd.read_excel("mannwhitney_redes.xlsx")

# Suponemos que las columnas se llaman 'Red X' y 'Red Y'
red_x = df['Red_X_ms'].dropna()
red_y = df['Red_Y_ms'].dropna()

# 2. Verificar no normalidad (Shapiro-Wilk y gráficos Q-Q)
print("Shapiro-Wilk Test:")
shapiro_x = stats.shapiro(red_x)
shapiro_y = stats.shapiro(red_y)
print(f"Red_X_ms: W = {shapiro_x.statistic:.4f}, p = {shapiro_x.pvalue:.4f}")
print(f"Red_Y_ms: W = {shapiro_y.statistic:.4f}, p = {shapiro_y.pvalue:.4f}")

# Gráficos Q-Q
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sm.qqplot(red_x, line='s', ax=axes[0])
axes[0].set_title("Q-Q Plot - Red_X_ms")
sm.qqplot(red_y, line='s', ax=axes[1])
axes[1].set_title("Q-Q Plot - Red_Y_ms")
plt.tight_layout()
plt.show()

# 3. Prueba de Mann-Whitney U (cola inferior: alternativa = 'less')
u_stat, p_value = stats.mannwhitneyu(red_x, red_y, alternative='less')

print("\nMann-Whitney U Test (cola inferior):")
print(f"U = {u_stat:.4f}")
print(f"p = {p_value:.4f}")

# 4. Interpretación
alpha = 0.05
if p_value < alpha:
    print("Se rechaza H₀: Hay evidencia de que la latencia de la Red X es menor que la de la Red Y.")
else:
    print("No se rechaza H₀: No hay evidencia suficiente para afirmar que la latencia de la Red X es menor.")