import pandas as pd
import numpy as np
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

# Inicialización de sesión
if "numero_datos" not in st.session_state:
    st.session_state.numero_datos = 10_000
if "full_dataset" not in st.session_state:
    st.session_state.full_dataset = False

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

# Vista de dataframe
f"Total datos: {len(df):,}"
st.dataframe(
    df,
    column_config={
        "person_age": st.column_config.NumberColumn(
            "Edad de la persona",
            format="%d año(s)",
        ),
        "person_income": st.column_config.NumberColumn(
            "Ingreso anual",
            format="$%.2d",
        ),
        "person_home_ownership": st.column_config.TextColumn(
            "Tipo de residencia",
        ),
        "person_emp_length": st.column_config.NumberColumn(
            "Años de actividad laboral",
            format="%d año(s)",
        ),
        "loan_amnt": st.column_config.NumberColumn(
            "Cantidad solicitada de crédito",
            format="$%d",
        ),
    },
)
columnas_tablas = st.columns(2)
with columnas_tablas[0]:
    st.dataframe(df.describe(include=['int', "float"]))
with columnas_tablas[1]:
    st.dataframe(df.describe(include=['category']))

# Vista de datos personales
columnas_persona = st.columns(2)
with columnas_persona[0]:
    "## Gráfico Tipo de residencia vs Estado de aprobación"
    fig=px.bar(
        df.groupby(['person_home_ownership', 'loan_status']).size().reset_index(name='count'),
        x="person_home_ownership",
        y="count",
        color="loan_status",
        barmode="group",
        labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'person_home_ownership': 'Tipo de Residencia'}
    )
    st.plotly_chart(fig)

with columnas_persona[1]:
    "## Gráfico Tipo de residencia vs Estado de aprobación"
    fig=px.bar(
        df.groupby(['loan_intent', 'loan_status']).size().reset_index(name='count'),
        x="loan_intent",
        y="count",
        color="loan_status",
        barmode="group",
        labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
    )
    st.plotly_chart(fig)

# Vista de datos categóricos del crédito
st_columnas_pie = st.columns(3)
with st_columnas_pie[0]:
    "## Intención del crédito"
    loan_intent_df = df['loan_intent'].value_counts().reset_index()
    loan_intent_df.columns = ["intent", "count"]
    fig = px.pie(loan_intent_df, values="count", names='intent', hole=.5)
    st.plotly_chart(fig)

with st_columnas_pie[1]:
    "## Grado del crédito"
    loan_grade_df = df['loan_grade'].value_counts().reset_index()
    loan_grade_df.columns = ["grade", "count"]
    fig = px.pie(loan_grade_df, values="count", names='grade', hole=.5)
    st.plotly_chart(fig)

with st_columnas_pie[2]:
    "## Estado del crédito"
    loan_status_df = df['loan_status'].value_counts().reset_index()
    loan_status_df.columns = ["status", "count"]
    loan_status_df['status'] = loan_status_df['status'].map({0: "Rechazado", 1: "Aprobado"})
    fig = px.pie(loan_status_df, values="count", names='status', hole=.5)
    st.plotly_chart(fig)

# Vista re relación entre ingreso de la persona y el total de crédito que solicita
# rel_income_amnt = pd.cut(df["person_income"], bins=40).value_counts()
# st.scatter_chart(df, x="person_income", y="loan_amnt")