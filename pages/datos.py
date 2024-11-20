import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st

"## Vista principal de los datos"

df = pd.read_csv("data/credit_risk_dataset.csv")
st.dataframe(df)

"## Describe"

st.dataframe(df.describe())

"## smt"

st.dataframe(df.describe(include=['object']))

"## Hists"

# columnas_numericas = df.select_dtypes(include=['int', 'float']).columns.tolist()
# opciones_plotting = st.multiselect(
#     "Escoja las variables a ver",
#     columnas_numericas,
#     [],
#     format_func=lambda t: t.replace("_", " ").capitalize()
# )

# if len(opciones_plotting) > 1:
#     fig, axes = plt.subplots(1, len(opciones_plotting), figsize=(5 * len(opciones_plotting), 4), constrained_layout=True)
#     for ax, col in zip(axes, opciones_plotting):
#         ax.hist(df[col], bins=10, color='skyblue', edgecolor='black')
#         ax.set_title(f'Histograma de {col}')
#         ax.set_xlabel(col)
#         ax.set_ylabel('Frecuencia')
#         ax.grid(axis='y', linestyle='--', alpha=0.7)

#     st.pyplot(fig)
# else:
#     "### Añada algo"

columnas_enteros = df.select_dtypes(include=['int']).columns.tolist()
columnas_flotantes = df.select_dtypes(include=['float']).columns.tolist()
columnas_numericas = columnas_enteros + columnas_flotantes
columnas_numericas_formateadas = list(map(lambda t: t.replace("_", " ").capitalize(), columnas_numericas))

plot_tabs = st.tabs(columnas_numericas_formateadas)
for tab, col in zip(plot_tabs, columnas_numericas):
    rango_columna: np.ndarray = None
    if col in columnas_enteros:
        rango_columna = np.arange(start=df[col].min(), stop=df[col].max())
    else:
        rango_columna = np.linspace(df[col].min(), df[col].max(), 100)

    filtro_minimo, filtro_maximo = tab.select_slider(
        "Selecciona un rango",
        options=rango_columna,
        format_func=lambda n: f'{round(n, 2):,}',
        value=(rango_columna.min(), rango_columna.max())
    )

    fig = px.histogram(df.loc[(df[col] >= filtro_minimo) & (df[col] <= filtro_maximo),col], nbins=20)
    tab.plotly_chart(fig, use_container_width=True)