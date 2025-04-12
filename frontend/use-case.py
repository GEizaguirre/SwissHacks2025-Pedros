import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import requests
    import urllib
    import re
    import sys
    import json
    mo.image(src="header-swiss.png")
    return json, mo, np, pd, plt, random, re, requests, sns, sys, urllib


@app.cell
def _(mo):
    mo.md(r"""## Use the predefined most used queries""")
    return


@app.cell
def _(json, requests, sys):
    if "pyodide" in sys.modules:
        from pyodide.http import pyfetch

        async def get_data(url):
            response = await pyfetch(url)
            json_str = await response.string()
            data = json.loads(json_str)
            return data

    else:

        def get_data(url):
            response = requests.get(url)
            return response.json()
    return get_data, pyfetch


@app.cell
def _():
    query1 = """
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

    query2 = """
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
    query3 = """
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
    query4 = """
    SELECT 
        Canton, 
        COUNT(*) AS num_rounds, 
        SUM(Amount) AS total_invested
    FROM deals
    WHERE Amount IS NOT NULL
    GROUP BY Canton
    ORDER BY num_rounds DESC;
    """
    query5 = """
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
    return query1, query2, query3, query4, query5


@app.cell
def _(mo, query1, query2, query3, query4, query5):
    # Minimal dropdown
    dropdown_dict = mo.ui.dropdown(options={"Q1":query1, "Q2":query2, "Q3":query3, "Q4":query4, "Q5":query5},
                            value="Q1", # initial value
                            label="Select your database query")
    return (dropdown_dict,)


@app.cell
def _(dropdown_dict, mo):
    mo.hstack([dropdown_dict])
    return


@app.cell
def _(dropdown_dict, urllib):
    query_encoded = urllib.parse.quote(dropdown_dict.value)
    return (query_encoded,)


@app.cell
async def _(get_data, pd, query_encoded, sys):
    query = f"http://127.0.0.1:5000/tables?query={query_encoded}"
    if "pyodide" in sys.modules:
        data = await get_data(query)
    else:
        data = get_data(query)
    df_queried = pd.DataFrame(data)
    return data, df_queried, query


@app.cell
def _(df_queried, plt, sns):
    def plot_1():
        fig, ax = plt.subplots(figsize=(8, 5))
        # Generar el gráfico con las columnas 'Value1' y 'Value2'
        pivot_rounds = df_queried.pivot(index='Year', columns='Phase', values='num_rounds').fillna(0)

        # Pivot para el total invertido
        pivot_invested = df_queried.pivot(index='Year', columns='Phase', values='total_invested').fillna(0)

        # Graficar dentro de la figura y eje creados
        pivot_rounds.plot(kind='line', marker='o', ax=ax)

        ax.set_title('Financing Rounds by Phase (hasta 2024)')
        ax.set_xlabel('Año')
        ax.set_ylabel('Número de Rondas')
        ax.grid(True)
        ax.legend(title='Phase')

        fig.tight_layout()
        return fig

    def plot_2():
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot_avg = df_queried.pivot(index='Year', columns='Phase', values='avg_invested').fillna(0)
        pivot_avg.plot(kind='line', marker='o', ax=ax)

        ax.set_title('Monto Promedio Invertido por Ronda (por Fase y Año, hasta 2024)')
        ax.set_xlabel('Año')
        ax.set_ylabel('Promedio Invertido (CHF)')
        ax.grid(True)
        ax.legend(title='Phase')

        fig.tight_layout()
        return fig


    def plot_3():
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_queried, x='total_invested', y='Industry', palette="viridis", ax=ax)

        ax.set_title('Capital Total Invertido por Industry')
        ax.set_xlabel('Capital Total Invertido (CHF)')
        ax.set_ylabel('Industry')

        fig.tight_layout()
        return fig


    def plot_4():
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_queried, x='num_rounds', y='Canton', palette="coolwarm", ax=ax)

        ax.set_title('Financing Rounds por Canton')
        ax.set_xlabel('Número de Rondas')
        ax.set_ylabel('Canton')

        fig.tight_layout()
        return fig


    def plot_5():
        fig, ax = plt.subplots(figsize=(8, 5))
        bins = range(
            int(df_queried['years_to_funding'].min()),
            int(df_queried['years_to_funding'].max()) + 2
        )

        sns.histplot(df_queried['years_to_funding'], kde=True, bins=bins, ax=ax)

        ax.set_title('Distribución: Años hasta la Primera Ronda de Financiación')
        ax.set_xlabel('Años para Conseguir la Primera Financiación')
        ax.set_ylabel('Cantidad de Startupd')

        fig.tight_layout()
        return fig


    def plot_6():
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df_queried['Year'], df_queried['cumulative_investment'], marker='o')

        ax.set_title('Evolución Acumulada del Capital Invertido (hasta 2024)')
        ax.set_xlabel('Año')
        ax.set_ylabel('Capital Invertido Acumulado (CHF)')
        ax.grid(True)

        fig.tight_layout()
        return fig

    def plot_selector(input):
        if input == "Q1":
            return plot_1
        elif input == "Q2":
            return plot_2
        elif input == "Q3":
            return plot_3
        elif input == "Q4":
            return plot_4
        elif input == "Q5":
            return plot_5
        elif input == "Q6":
            return plot_6
        else:
            raise ValueError("Input must be one of 'Q1' to 'Q6'")
    return plot_1, plot_2, plot_3, plot_4, plot_5, plot_6, plot_selector


@app.cell
def _(dropdown_dict, plot_selector):
    plot_to_display = plot_selector(dropdown_dict.selected_key)
    plot_to_display()
    return (plot_to_display,)


@app.cell
def _(mo):
    mo.md(r"""## Custom queries to SQL database""")
    return


@app.cell
def _(np, pd):
    def get_dummy_df():
        # Crear un DataFrame dummy con datos aleatorios
        data = {
            'Date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
            'Value1': np.random.rand(10) * 100,
            'Value2': np.random.rand(10) * 100
        }

        # Convertir el diccionario en un DataFrame
        df = pd.DataFrame(data)
        return df
    return (get_dummy_df,)


@app.cell
def _(mo):
    sql_editor = mo.ui.code_editor(language="sql", value="select * from users;")
    sql_editor
    return (sql_editor,)


@app.cell
def _(mo):
    fetch_button = mo.ui.run_button(label="Fetch query")
    fetch_button
    return (fetch_button,)


@app.cell
def _(fetch_button, get_dummy_df, mo):
    mo.stop(not fetch_button.value)
    df = get_dummy_df()
    df
    return (df,)


@app.cell
def _(mo):
    plot_editor = mo.ui.code_editor(language="python", value="""def plot_custom():
        fig, ax = plt.subplots(figsize=(8, 5))

        # Generar el gráfico con las columnas 'Value1' y 'Value2'
        ax.plot(df['Date'], df['Value1'], label='Value1', marker='o', color='b')
        ax.plot(df['Date'], df['Value2'], label='Value2', marker='x', color='r')

        # Añadir título y etiquetas
        ax.set_title("Random Plot of Values Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")

        # Mostrar leyenda
        ax.legend()

        # Retornar la figura
        return fig
    """)
    plot_editor
    return (plot_editor,)


@app.cell
def _(mo):
    plot_button = mo.ui.run_button(label="Generate plot")
    plot_button
    return (plot_button,)


@app.cell
def _(mo, plot_button, plot_custom, plot_editor):
    mo.stop(not plot_button.value)
    exec(plot_editor.value)
    plot_custom()
    return


if __name__ == "__main__":
    app.run()
