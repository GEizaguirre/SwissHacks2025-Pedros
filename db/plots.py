import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Conexión a la base de datos ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='svcr-db'
)

# Configuración de Seaborn para los gráficos
sns.set(style="whitegrid")

# =============================================================================
# 1. Financing Rounds y Capital Total por Fase y Año (hasta 2024)
# =============================================================================

# Se filtran las rows donde Phase es nulo o 'nan'
query_rounds = """
SELECT 
    YEAR(`Date of the funding round`) AS Year, 
    Phase, 
    COUNT(*) AS num_rounds, 
    SUM(Amount) AS total_invested
FROM deals
WHERE YEAR(`Date of the funding round`) <= 2024
  AND Phase IS NOT NULL
  AND Phase <> 'nan'
GROUP BY Year, Phase
ORDER BY Year, Phase;
"""
df_rounds = pd.read_sql(query_rounds, conn)

# Creamos pivot tables para graficar
# Pivot para el número de rondas
pivot_rounds = df_rounds.pivot(index='Year', columns='Phase', values='num_rounds').fillna(0)

# Pivot para el total invertido
pivot_invested = df_rounds.pivot(index='Year', columns='Phase', values='total_invested').fillna(0)

# Plot: Número de financing rounds por fase (línea de tiempo)

pivot_rounds.plot(kind='line', marker='o')
plt.title('Financing Rounds by Phase (hasta 2024)')
plt.xlabel('Año')
plt.ylabel('Número de Rondas')
plt.grid(True)
plt.legend(title='Phase')
plt.tight_layout()
plt.show()

# Plot: Capital invertido por fase (línea de tiempo)

pivot_invested.plot(kind='line', marker='o')
plt.title('Capital Invertido by Phase (hasta 2024)')
plt.xlabel('Año')
plt.ylabel('Capital Invertido Total (CHF)')
plt.grid(True)
plt.legend(title='Phase')
plt.tight_layout()
plt.show()


# =============================================================================
# 2. Monto Promedio Invertido por Ronda según Fase y Año
# =============================================================================

query_avg = """
SELECT 
    YEAR(`Date of the funding round`) AS Year, 
    Phase, 
    AVG(Amount) AS avg_invested
FROM deals
WHERE Amount IS NOT NULL 
  AND YEAR(`Date of the funding round`) <= 2024
  AND Phase IS NOT NULL
  AND Phase <> 'nan'
GROUP BY Year, Phase
ORDER BY Year, Phase;
"""
df_avg = pd.read_sql(query_avg, conn)

# Generamos una pivot table para graficar el promedio invertido
pivot_avg = df_avg.pivot(index='Year', columns='Phase', values='avg_invested').fillna(0)


pivot_avg.plot(kind='line', marker='o')
plt.title('Monto Promedio Invertido por Ronda (por Fase y Año, hasta 2024)')
plt.xlabel('Año')
plt.ylabel('Promedio Invertido (CHF)')
plt.grid(True)
plt.legend(title='Phase')
plt.tight_layout()
plt.show()


# =============================================================================
# 3. Distribución de Inversión por Industry
# Relaciona la tabla deals con companies para ver en qué sectores se invierte más.
# =============================================================================

query_industry = """
SELECT 
    c.Industry, 
    COUNT(d.Id) AS num_rounds, 
    SUM(d.Amount) AS total_invested
FROM deals d
JOIN companies c ON c.Title = d.Company
WHERE d.Amount IS NOT NULL
GROUP BY c.Industry
ORDER BY total_invested DESC;
"""
df_industry = pd.read_sql(query_industry, conn)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_industry, x='total_invested', y='Industry', palette="viridis")
plt.title('Capital Total Invertido por Industry')
plt.xlabel('Capital Total Invertido (CHF)')
plt.ylabel('Industry')
plt.tight_layout()
plt.show()


# =============================================================================
# 4. Distribución de Financing Rounds por Canton
# Se observa la cantidad de rondas y la inversión total por cantón.
# =============================================================================

query_canton = """
SELECT 
    Canton, 
    COUNT(*) AS num_rounds, 
    SUM(Amount) AS total_invested
FROM deals
WHERE Amount IS NOT NULL
GROUP BY Canton
ORDER BY num_rounds DESC;
"""
df_canton = pd.read_sql(query_canton, conn)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_canton, x='num_rounds', y='Canton', palette="coolwarm")
plt.title('Financing Rounds por Canton')
plt.xlabel('Número de Rondas')
plt.ylabel('Canton')
plt.tight_layout()
plt.show()


# =============================================================================
# 5. Tiempo hasta la Primera Ronda de Financiación
# Calcula la diferencia entre el año de fundación y el año del primer deal.
# =============================================================================

query_time_to_funding = """
SELECT 
    c.Title, 
    c.Year AS founding_year, 
    MIN(YEAR(d.`Date of the funding round`)) AS first_funding_year,
    MIN(YEAR(d.`Date of the funding round`)) - c.Year AS years_to_funding
FROM companies c
JOIN deals d ON c.Title = d.Company
GROUP BY c.Title, c.Year
HAVING first_funding_year IS NOT NULL
ORDER BY years_to_funding;
"""
df_time = pd.read_sql(query_time_to_funding, conn)

plt.figure(figsize=(10, 6))
sns.histplot(df_time['years_to_funding'], kde=True,
             bins=range(int(df_time['years_to_funding'].min()), int(df_time['years_to_funding'].max()) + 2))
plt.title('Distribución: Años hasta la Primera Ronda de Financiación')
plt.xlabel('Años para Conseguir la Primera Financiación')
plt.ylabel('Cantidad de Startups')
plt.tight_layout()
plt.show()


# =============================================================================
# 6. Evolución Acumulada del Capital Invertido a lo largo del Tiempo
# Muestra cómo se ha acumulado la inversión año a año (hasta 2024).
# =============================================================================

query_yearly = """
SELECT 
    YEAR(`Date of the funding round`) AS Year, 
    SUM(Amount) AS yearly_invested
FROM deals
WHERE YEAR(`Date of the funding round`) <= 2024
GROUP BY YEAR(`Date of the funding round`)
ORDER BY Year;
"""
df_yearly = pd.read_sql(query_yearly, conn)

# Ordenar por año y calcular la inversión acumulada
df_yearly = df_yearly.sort_values('Year')
df_yearly['cumulative_investment'] = df_yearly['yearly_invested'].cumsum()

plt.plot(df_yearly['Year'], df_yearly['cumulative_investment'], marker='o')
plt.title('Evolución Acumulada del Capital Invertido (hasta 2024)')
plt.xlabel('Año')
plt.ylabel('Capital Invertido Acumulado (CHF)')
plt.grid(True)
plt.tight_layout()
plt.show()


# Cerramos la conexión a la base de datos
conn.close()
