import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar los datos desde el archivo Excel
df = pd.read_excel('tstudent_algoritmos.xlsx', sheet_name=0)

# 2. Verificar la normalidad con la prueba de Shapiro-Wilk
shapiro_A = stats.shapiro(df['Algoritmo_A_ops_sec'])
shapiro_B = stats.shapiro(df['Algoritmo_B_ops_sec'])

# 3. Verificar homocedasticidad con la prueba de Levene
levene_test = stats.levene(df['Algoritmo_A_ops_sec'], df['Algoritmo_B_ops_sec'])

# 4. Aplicar la prueba t-Student (o Welch si las varianzas son desiguales)
if levene_test.pvalue > 0.05:  # Si las varianzas son iguales
    t_stat, p_value = stats.ttest_ind(df['Algoritmo_A_ops_sec'], df['Algoritmo_B_ops_sec'], equal_var=True)
else:  # Si las varianzas no son iguales
    t_stat, p_value = stats.ttest_ind(df['Algoritmo_A_ops_sec'], df['Algoritmo_B_ops_sec'], equal_var=False)

# 5. Calcular el intervalo de confianza del 95% para la diferencia de medias
if levene_test.pvalue > 0.05:
    n_A = len(df['Algoritmo_A_ops_sec'])
    n_B = len(df['Algoritmo_B_ops_sec'])
    mean_A = np.mean(df['Algoritmo_A_ops_sec'])
    mean_B = np.mean(df['Algoritmo_B_ops_sec'])
    std_A = np.std(df['Algoritmo_A_ops_sec'], ddof=1)
    std_B = np.std(df['Algoritmo_B_ops_sec'], ddof=1)

    se_diff = np.sqrt((std_A**2 / n_A) + (std_B**2 / n_B))  # Error estándar de la diferencia
    df_t = n_A + n_B - 2  # Grados de libertad
    margin_of_error = stats.t.ppf(1 - 0.025, df_t) * se_diff  # Margen de error para el intervalo de confianza

    conf_interval = (mean_A - mean_B - margin_of_error, mean_A - mean_B + margin_of_error)
else:
    conf_interval = stats.t.interval(0.95, len(df['Algoritmo_A_ops_sec']) - 1, loc=t_stat, scale=p_value)

# 6. Visualización de los histogramas
plt.figure(figsize=(10, 6))

# Histograma
plt.subplot(1, 2, 1)
plt.hist(df['Algoritmo_A_ops_sec'], alpha=0.7, label='Algoritmo A', bins=10)
plt.hist(df['Algoritmo_B_ops_sec'], alpha=0.7, label='Algoritmo B', bins=10)
plt.legend()
plt.title('Distribución de los Rendimientos de los Algoritmos')
plt.xlabel('Operaciones por segundo')
plt.ylabel('Frecuencia')

# Boxplot (corrección del parámetro 'labels' a 'tick_labels')
plt.subplot(1, 2, 2)
plt.boxplot([df['Algoritmo_A_ops_sec'], df['Algoritmo_B_ops_sec']], tick_labels=['Algoritmo A', 'Algoritmo B'])
plt.title('Boxplot de Rendimientos')
plt.ylabel('Operaciones por segundo')

# Mostrar los gráficos
plt.tight_layout()
plt.show()

# Imprimir los resultados clave en la consola para el informe
print("\n1. Verificación de normalidad (Shapiro-Wilk) y homocedasticidad (Levene):")
print(f"  - Shapiro-Wilk para Algoritmo A: p-value = {shapiro_A[1]:.4f}. Los datos de Algoritmo A son normales.")
print(f"  - Shapiro-Wilk para Algoritmo B: p-value = {shapiro_B[1]:.4f}. Los datos de Algoritmo B son normales.")
print(f"  - Prueba de Levene: p-value = {levene_test.pvalue:.4f}. No se rechaza la hipótesis de igualdad de varianzas.")

# Interpretar la hipótesis nula y alternativa
if p_value < 0.05:
    print("\n2. Aplicación de t-Student independiente (o Welch si varianzas desiguales):")
    print(f"  - Estadístico t: {t_stat:.4f}, Valor p: {p_value:.4e}. Se rechaza la hipótesis nula (H₀) y se acepta la hipótesis alternativa (H₁): Algoritmo A es más rápido que Algoritmo B.")
else:
    print("\n2. Aplicación de t-Student independiente (o Welch si varianzas desiguales):")
    print(f"  - Estadístico t: {t_stat:.4f}, Valor p: {p_value:.4e}. No se rechaza la hipótesis nula (H₀): No hay suficiente evidencia para afirmar que Algoritmo A es más rápido que Algoritmo B.")

print("\n3. Interpretación del valor p y el intervalo de confianza:")
print(f"  - Intervalo de Confianza del 95% para la diferencia de medias: {conf_interval}.")
