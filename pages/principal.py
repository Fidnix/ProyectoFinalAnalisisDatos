import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# COnfiguración de página
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# Dataframe
@st.cache_data
def obtener_df(path, full_dataset=False, subsize = 10_000):
    pd.set_option("styler.render.max_elements", 390972)
    df = pd.read_csv(path)
    if not full_dataset:
        df = df.sample(subsize).reset_index()
        df = df.drop("index", axis=1)
    df["loan_intent"] = df["loan_intent"].astype("category")
    df["person_home_ownership"] = df["person_home_ownership"].astype("category")
    df["loan_grade"] = df["loan_grade"].astype("category")
    df["cb_person_default_on_file"] = df["cb_person_default_on_file"].astype("category")
    df["loan_status_cat"] = df['loan_status'].map({0: 'cumplido', 1: 'moroso'})
    bins = np.linspace(18,100,6).round()
    labels = ['muy joven', 'joven', 'maso', 'viejo', 'muy viejo']

    # Crear la nueva columna categórica
    df['edades'] = pd.cut(df['person_age'], bins=bins, labels=labels, right=False)
    return df

# @st.cache_data(show_spinner="Estilisando datos")
# def obtener_estilisado_df(df):
#     return df.style.apply(lambda cell, props="": np.where(cell == 0, props, ""), props="color:red",axis=0, subset=["loan_status"]).apply(lambda cell, props="": np.where(cell == 1, props, ""), props="color:green",axis=0, subset=["loan_status"])

plot_labels = {
    'loan_grade': 'Estado del crédito',
    'count': 'Cantidad',
    'loan_intent': 'Intención de crédito',
    "person_home_ownership": "Tipo de residencia"
}

# Título
"""
# Vista principal de los datos
---
"""

# ==================================
# Configuración de visualización
# ==================================

# Funciones
# Estas funciones permiten cambiar la sesión para la visualización de datos
def cambiar_numero_sesion():
    st.session_state.numero_datos = st.session_state.input_number
def cambiar_full_dataset_sesion():
    st.session_state.full_dataset = st.session_state.input_full_dataset
def cambiar_outliers_sesion():
    st.session_state.outliers = st.session_state.input_outliers

# Inicialización de sesión
if "numero_datos" not in st.session_state:
    st.session_state.numero_datos = 10_000
if "full_dataset" not in st.session_state:
    st.session_state.full_dataset = False
if "outliers" not in st.session_state:
    st.session_state.outliers = True

# Maquetación del contenedor de configuración
with st.container(border=True):
    columnas_configuracion = st.columns(2)
    with columnas_configuracion[0]:
        st.checkbox(
            "Usar todo el dataset",
            key="input_full_dataset",
            value=st.session_state.full_dataset,
            help="Usar todo el dataset. Usar esta opción solo cuando se tenga buena computación y se requiera analizar los datos sin márgenes de error",
            on_change=cambiar_full_dataset_sesion
        )
        st.checkbox(
            "Habilitar outliers",
            key="input_outliers",
            value=st.session_state.outliers,
            help="Ignorar los registros con outliers",
            on_change=cambiar_outliers_sesion
        )
    with columnas_configuracion[1]:
        print(st.session_state.numero_datos)
        st.number_input(
            "Número de datos a usar",
            min_value=0,
            max_value=20_000,
            key = "input_number",
            value=st.session_state.numero_datos,
            disabled=st.session_state.full_dataset,
            on_change=cambiar_numero_sesion
        )

# Dataset a usar
df = obtener_df("data/credit_risk_dataset.csv", st.session_state.full_dataset, st.session_state.numero_datos)

# ==========================================
# Parte de Fidel
# ==========================================

"# Estimación de ingresos por créditos"

seleccion_ganancias_grade = st.pills(
    "Seleccione los grados",
    options=df["loan_grade"].unique(),
    default=df["loan_grade"].unique(),
    selection_mode="multi"
)

intereses_generados_no_morosos = ((df.loc[(df["loan_grade"].isin(seleccion_ganancias_grade)) & (df["loan_status"]  ==  0),"loan_int_rate"]/100 + 1) * df["loan_amnt"]).sum()
intereses_generados_morosos = ((df.loc[(df["loan_grade"].isin(seleccion_ganancias_grade)) & (df["loan_status"]  ==  1),"loan_int_rate"]/100 + 1) * df["loan_amnt"]).sum()

columnas_ingresos = st.columns(2)

with columnas_ingresos[0].container(border=True):
    "## Ganancias estimadas"
    f"### ${intereses_generados_no_morosos:,.{2}f}"

with columnas_ingresos[1].container(border=True):
    "## Pérdidas estimadas"
    f"### -${intereses_generados_morosos:,.{2}f}"

with st.container(border=True):
    "## Neto estimado"
    f"### ${intereses_generados_no_morosos - intereses_generados_morosos:,.{2}f}"

# Matriz de confusión para historial

# grouped = df.groupby(["cb_person_default_on_file", "loan_status_cat"]).size().reset_index(name="count")

# table_2x2 = pd.pivot_table(
#     grouped,
#     values="count",
#     index="cb_person_default_on_file",  # Filas
#     columns="loan_status_cat",          # Columnas
#     fill_value=0                        # Rellenar valores nulos con 0
# )
# fig = make_subplots(
#     rows=1, cols=1,
#     shared_xaxes=True,
#     vertical_spacing=0.03,
#     specs=[[{"type": "table"}],
# )

# # Mostrar como gráfico en Plotly
# fig = go.Figure(data=[go.Table(
#     header=dict(
#         values=[""] + table_2x2.columns.tolist(),  # Etiquetas de columnas
#         fill_color="lightgrey",
#         align="center"
#     ),
#     cells=dict(
#         values=[table_2x2.index] + [table_2x2[col] for col in table_2x2.columns],  # Datos por columna
#         fill_color="white",
#         align="center"
#     )
# )])

# st.plotly_chart(fig)

# Vista de datos personales
columnas_persona = st.columns(2, gap="large")
with columnas_persona[0]:
    "## Gráfico Tipo de residencia vs Estado de aprobación"
    fig=px.bar(
        df.groupby(['person_home_ownership', 'loan_status_cat']).size().reset_index(name='count'),
        x="person_home_ownership",
        y="count",
        color="loan_status_cat",
        barmode="group",
        labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'person_home_ownership': 'Tipo de Residencia'}
    )
    st.plotly_chart(fig)

with columnas_persona[1]:
    "## Gráfico Tipo de residencia vs Estado de aprobación"
    fig=px.bar(
        df.groupby(['loan_intent', 'loan_status_cat']).size().reset_index(name='count'),
        x="loan_intent",
        y="count",
        color="loan_status_cat",
        barmode="group",
        labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
    )
    st.plotly_chart(fig)

# Vista de datos categóricos del crédito

"## Gráficos de pie respecto al cumplimiento de un crédito"
st_columnas_pie = st.columns(2)
with st_columnas_pie[0]:
    "### Intención del crédito"
    loan_intent_df = df['loan_intent'].value_counts().reset_index()
    loan_intent_df.columns = ["intent", "count"]
    fig = px.pie(loan_intent_df, values="count", names='intent', hole=.5)
    st.plotly_chart(fig)

with st_columnas_pie[1]:
    "### Grado del crédito"
    loan_grade_df = df.loc[df["loan_status"]==1,'loan_grade'].value_counts().reset_index()
    loan_grade_df.columns = ["grade", "count"]
    fig = px.pie(loan_grade_df, values="count", names='grade', hole=.5)
    st.plotly_chart(fig)

# Grado de crédito vs Residencia

"## Grado de crédito vs Residencia"
columnas_smt = st.columns(2)
with columnas_smt[0]:
    "### Clientes morosos"
    fig=px.bar(
        df.loc[df["loan_status"]==1,:].groupby(['loan_grade', "person_home_ownership"]).size().reset_index(name='count'),
        x="loan_grade",
        y="count",
        color="person_home_ownership",
        barmode="group",
        labels=plot_labels
    )
    st.plotly_chart(fig)

with columnas_smt[1]:
    "### Clientes no morosos"
    fig=px.bar(
        df.loc[df["loan_status"]==0,:].groupby(['loan_grade', "person_home_ownership"]).size().reset_index(name='count'),
        x="loan_grade",
        y="count",
        color="person_home_ownership",
        barmode="group",
        labels=plot_labels
    )
    st.plotly_chart(fig)

# "## Cantidad de pagos cumplidos respecto a la edad de las personas"

# tags_edades = st.pills(
#     "Seleccione el grupo de edad para filtrar",
#     options=df["edades"].unique(),
#     default=df["edades"].unique(),
#     selection_mode="multi"
# )

# fig=px.bar(
#     df.loc[df["edades"].isin(tags_edades), :].groupby(['edades', "loan_status_cat"]).size().reset_index(name='count'),
#     x="edades",
#     y="count",
#     color="loan_status_cat",
#     barmode="group",
#     labels=plot_labels
# )
# st.plotly_chart(fig)

# ==========================================
# Parte de Daniel
# ==========================================

"## Razón de creditaje de clientes morosos"

tags_intent = st.pills(
    "Seleccione el grupo de edad para filtrar",
    options=df["loan_intent"].unique(),
    default=df["loan_intent"].unique(),
    selection_mode="multi"
)

#grafico de cantidad de morosos dividido por intencion de credito

df_filtrado = df[(df['loan_status'] == 1) & (df["loan_intent"].isin(tags_intent))]
fig = px.bar(
    df_filtrado.groupby(['loan_intent']).size().reset_index(name='count'),
    x="loan_intent",
    y="count",
    labels={'loan_intent': 'Intención de crédito', 'count': 'Cantidad'},
    title="Intencion de crédito de los clientes morosos"
)

st.plotly_chart(fig)

"## Clientes morosos por rango de edad"

#grafico de cantidad de morosos dividido por grupo de edades

#rangos de edad
bins = list(range(18, 100, 10))  # Rango de 18 a 100 anios con intervalos de 10 anios
labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]  # Etiquetas como "18-28", "28-38", etc.

#morosos
df_filtrado = df[df['loan_status'] == 1]

#nueva columna para los rangos de edad
df_filtrado['age_range'] = pd.cut(df_filtrado['person_age'], bins=bins, labels=labels, right=False)

#agrupar por rango de edad
df_agrupado = df_filtrado.groupby(['age_range']).size().reset_index(name='count')

#gráfico de barras
fig = px.bar(
    df_agrupado,
    x="age_range",
    y="count",
    labels={'age_range': 'Rango de Edad', 'count': 'Cantidad de Clientes'},
    title="Morosos por Rango de Edad"
)
st.plotly_chart(fig)