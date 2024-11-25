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
    
    # Calcular IQR para filtrar outliers en person_income
    Q1 = df['person_income'].quantile(0.25)
    Q3 = df['person_income'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filtrar valores dentro del rango intercuartil
    df = df[(df['person_income'] >= lower_bound) & (df['person_income'] <= upper_bound)]
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
columnas_persona = st.columns(2, gap="large")
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
    loan_grade_df = df.loc[df["loan_status"]==1,'loan_grade'].value_counts().reset_index()
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
"## Gráfico de Tipo de residencia vs relación de crédito - ingreso"

fig = px.box(
        df,
        x="person_home_ownership", y="loan_percent_income",
        labels={'person_home_ownership': 'Tipo de residencia', 'loan_percent_income': 'Relación crédito - Ingresos'}
    )
st.plotly_chart(fig)

"# Gráfico de Tipo de residencia vs Cantidad solicitada de crédito e Ingresos anuales"
st.bar_chart(df, x="person_home_ownership", y=["person_income", "loan_amnt"], horizontal=True, x_label="Tipo de residencia", y_label="Count")

# =========================================

# fig = go.Figure()
# fig.add_trace(go.Bar(
#     x=months,
#     y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
#     name='Primary Product',
#     marker_color='indianred'
# ))
# fig.add_trace(go.Bar(
#     x=months,
#     y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
#     name='Secondary Product',
#     marker_color='lightsalmon'
# ))

# # Here we modify the tickangle of the xaxis, resulting in rotated labels.
# fig.update_layout(barmode='group', xaxis_tickangle=-45)
# fig.show()

fig=px.bar(
    df.loc[df["loan_status"]==1,:].groupby(['loan_grade', "person_home_ownership"]).size().reset_index(name='count'),
    x="loan_grade",
    y="count",
    color="person_home_ownership",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)


fig=px.bar(
    df.loc[df["loan_status"]==0,:].groupby(['loan_grade', "person_home_ownership"]).size().reset_index(name='count'),
    x="loan_grade",
    y="count",
    color="person_home_ownership",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## OTro grafico"

fig=px.bar(
df.loc[df["loan_status"]==1,:].groupby(['person_home_ownership']).size().reset_index(name='count'),
    x="person_home_ownership",
    y="count",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## asdazdasd"

columnas_nose = st.columns(2)

with columnas_nose[0]:
    "## Loan status == 0"
    fig=px.histogram(
        df[df["loan_status"]==0],
        x="loan_percent_income",
        nbins=100,
        opacity=.7
    )
    st.plotly_chart(fig)
with columnas_nose[1]:
    "## Loan status == 1"
    fig=px.histogram(
        df[df["loan_status"]==1],
        x="loan_percent_income",
        nbins=100,
        opacity=.7
    )
    st.plotly_chart(fig)

fig=px.histogram(
    df,
    x="loan_percent_income",
    nbins=100,
    color="loan_status",
    barmode="overlay",
    opacity=.7
)
st.plotly_chart(fig)

"## Otras cosas"

fig=px.bar(
    df.groupby(['loan_grade', "loan_status_cat"]).size().reset_index(name='count'),
    x="loan_grade",
    y="count",
    color="loan_status_cat",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

# TODO: Filtro de edades mediante tags

fig=px.bar(
    df.groupby(['edades', "loan_status_cat"]).size().reset_index(name='count'),
    x="edades",
    y="count",
    color="loan_status_cat",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## viviendas por edades"
fig=px.bar(
    df.groupby(['edades', 'person_home_ownership']).size().reset_index(name='count'),
    x="edades",
    y="count",
    color="person_home_ownership",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## Viviendas por credito aprobado"
fig=px.bar(
    df.groupby(['person_home_ownership', "loan_status_cat"]).size().reset_index(name='count'),
    x="person_home_ownership",
    y="count",
    color="loan_status_cat",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## Ingresos por edades"
fig=px.bar(
    df.groupby(['edades', 'person_income', "loan_status_cat"]).size().reset_index(name='count'),
    x="edades",
    y="count",
    color="person_income",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

"## Ingresos por credito aprobado"
fig=px.bar(
    df.groupby(['person_income', "loan_status_cat"]).size().reset_index(name='count'),
    x="person_income",
    y="count",
    color="loan_status_cat",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)

st.dataframe(df.groupby(["cb_person_default_on_file", "loan_status_cat"]).size())