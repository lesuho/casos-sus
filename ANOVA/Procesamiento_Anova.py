import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 1. Cargar los datos desde el archivo Excel
df = pd.read_excel('anova_cifrado.xlsx', sheet_name=0)

# 2. Verificar la normalidad con la prueba de Shapiro-Wilk para cada algoritmo
shapiro_AES = stats.shapiro(df['AES_256'])
shapiro_RSA = stats.shapiro(df['RSA_2048'])
shapiro_ChaCha = stats.shapiro(df['ChaCha20'])

# 3. Verificar homocedasticidad con la prueba de Levene
levene_test = stats.levene(df['AES_256'], df['RSA_2048'], df['ChaCha20'])

# 4. Aplicar ANOVA de una vía
anova_result = stats.f_oneway(df['AES_256'], df['RSA_2048'], df['ChaCha20'])

# 5. Interpretación de ANOVA
if anova_result.pvalue < 0.05:
    anova_interpretation = "Se rechaza la hipótesis nula (H₀), lo que indica que hay diferencias significativas entre los algoritmos."
else:
    anova_interpretation = "No se rechaza la hipótesis nula (H₀), lo que sugiere que no hay diferencias significativas entre los algoritmos."

# 6. Realizar el post-hoc de Tukey si ANOVA es significativo
tukey_result = None
if anova_result.pvalue < 0.05:
    # Transformar el DataFrame para hacer el análisis post-hoc
    df_melted = df.melt(value_name="CPU", var_name="Algorithm")
    tukey_result = pairwise_tukeyhsd(df_melted["CPU"], df_melted["Algorithm"])

# 7. Gráficos
plt.figure(figsize=(14, 6))

# Boxplot para visualizar las diferencias
plt.subplot(1, 2, 1)
plt.boxplot([df['AES_256'], df['RSA_2048'], df['ChaCha20']], tick_labels=['AES-256', 'RSA-2048', 'ChaCha20'])
plt.title('Comparación del Consumo de CPU entre Algoritmos')
plt.ylabel('Consumo de CPU (%)')
plt.xlabel('Algoritmos de Cifrado')

# Histograma para visualizar la distribución de los datos
plt.subplot(1, 2, 2)
plt.hist(df['AES_256'], alpha=0.7, label='AES-256', bins=10, color='blue')
plt.hist(df['RSA_2048'], alpha=0.7, label='RSA-2048', bins=10, color='orange')
plt.hist(df['ChaCha20'], alpha=0.7, label='ChaCha20', bins=10, color='green')
plt.legend()
plt.title('Distribución del Consumo de CPU de los Algoritmos')
plt.xlabel('Consumo de CPU (%)')
plt.ylabel('Frecuencia')

# Mostrar los gráficos
plt.tight_layout()
plt.show()

# Imprimir los resultados clave con notación científica
print("\nResultados de la Prueba de Normalidad:")
print(f"Shapiro-Wilk para AES-256: p-value = {shapiro_AES[1]:.4e}")
print(f"Shapiro-Wilk para RSA-2048: p-value = {shapiro_RSA[1]:.4e}")
print(f"Shapiro-Wilk para ChaCha20: p-value = {shapiro_ChaCha[1]:.4e}")

print("\nResultado de la Prueba de Levene (Homocedasticidad):")
print(f"p-value de Levene: {levene_test.pvalue:.4e}")

print("\nResultado de ANOVA de una vía:")
print(f"F-statistic: {anova_result.statistic:.4f}, p-value: {anova_result.pvalue:.4e}")
print(f"\nInterpretación de ANOVA: {anova_interpretation}")

# Resultados de Tukey si ANOVA es significativo
if tukey_result:
    print("\nResultados Post-hoc (Tukey):")
    print(tukey_result.summary())
else:
    print("\nNo se realizó el test post-hoc de Tukey debido a un ANOVA no significativo.")
