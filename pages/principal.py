import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
    bins = np.linspace(18,100,6).round(2) # Límite de edades
    labels = ['muy joven', 'joven', 'maso', 'viejo', 'muy viejo']

    # Crear la nueva columna categórica
    df['edades'] = pd.cut(df['person_age'], bins=bins, labels=labels, right=False)
    return df

# @st.cache_data(show_spinner="Estilisando datos")
# def obtener_estilisado_df(df):
#     return df.style.apply(lambda cell, props="": np.where(cell == 0, props, ""), props="color:red",axis=0, subset=["loan_status"]).apply(lambda cell, props="": np.where(cell == 1, props, ""), props="color:green",axis=0, subset=["loan_status"])

# Título
"# Vista principal de los datos"

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