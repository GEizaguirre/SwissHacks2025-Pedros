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
    import requests
    mo.image(src="header-swiss.png")
    return mo, np, pd, plt, random, requests


@app.cell
def _():
    # Dummy queries
    query1 = "SELECT * FROM cars"
    query2 = "SELECT * FROM houses"
    query3 = "SELECT * FROM pens"
    query4 = "SELECT * FROM routers"
    query5 = "SELECT * FROM streets"
    return query1, query2, query3, query4, query5


@app.cell(hide_code=True)
def _(mo, query1, query2, query3, query4, query5):
    # Minimal dropdown
    dropdown_dict = mo.ui.dropdown(options={"Q1":query1, "Q2":query2, "Q3":query3, "Q4":query4, "Q5":query5},
                            value="Q1", # initial value
                            label="Select your database query")
    return (dropdown_dict,)


@app.cell
def _(mo):
    mo.md(r"""## Use the prefenined most used queries""")
    return


@app.cell
def _(dropdown_dict, mo):
    mo.hstack([dropdown_dict])
    return


@app.cell(hide_code=True)
def _():
    # requests.get(f"https://random-word-api.herokuapp.com/word?number={dropdown_dict.selected_key[-1]}").json()
    return


@app.cell(hide_code=True)
def _(np, plt):
    def line_plot():
        fig, ax = plt.subplots(figsize=(8,5))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_title("Line Plot")
        ax.set_xlabel("x")
        ax.set_ylabel("sin(x)")
        ax.grid(True)
        return fig

    def bar_plot():
        fig, ax = plt.subplots(figsize=(8,5))
        categories = ['A', 'B', 'C', 'D']
        values = [10, 15, 7, 12]
        ax.bar(categories, values)
        ax.set_title("Bar Plot")
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        return fig

    def scatter_plot():
        fig, ax = plt.subplots(figsize=(8,5))
        x = np.random.rand(50)
        y = np.random.rand(50)
        ax.scatter(x, y, c='red', alpha=0.5)
        ax.set_title("Scatter Plot")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        return fig

    def histogram():
        fig, ax = plt.subplots(figsize=(8,5))
        data = np.random.randn(1000)
        ax.hist(data, bins=30, edgecolor='black')
        ax.set_title("Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        return fig

    def pie_chart():
        sizes = [25, 35, 20, 20]
        labels = ['Apple', 'Banana', 'Cherry', 'Date']
        fig, ax = plt.subplots(figsize=(8,5))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title("Pie Chart")
        ax.axis('equal')
        return fig

    def plot_selector(input):
        if input == "Q1":
            return line_plot
        elif input == "Q2":
            return bar_plot
        elif input == "Q3":
            return scatter_plot
        elif input == "Q4":
            return histogram
        elif input == "Q5":
            return pie_chart
        else:
            raise ValueError("Input must be one of 'Q1' to 'Q5'")
    return (
        bar_plot,
        histogram,
        line_plot,
        pie_chart,
        plot_selector,
        scatter_plot,
    )


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
