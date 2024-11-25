import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from utils.obtener_data import obtener_df

# COnfiguración de página
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)
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
# Dashboard riesgo de crédito 💸
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
df, ord_encs = obtener_df("data/credit_risk_dataset.csv", st.session_state.full_dataset, st.session_state.numero_datos)

# ==========================================
# Parte de Fidel
# ==========================================

"# Estimación de ingresos por créditos"
seleccion_ganancias_grade = st.pills(
    "Seleccione los grados",
    options=np.sort(df["loan_grade"].unique()),
    default=df["loan_grade"].unique(),
    selection_mode="multi"
)
intereses_generados_no_morosos = ((df.loc[(df["loan_grade"].isin(seleccion_ganancias_grade)) & (df["loan_status"]  ==  0),"loan_int_rate"]/100 + 1) * df["loan_amnt"]).sum()
intereses_generados_morosos = ((df.loc[(df["loan_grade"].isin(seleccion_ganancias_grade)) & (df["loan_status"]  ==  1),"loan_int_rate"]/100 + 1) * df["loan_amnt"]).sum()

columnas_ingresos = st.columns(2)

with columnas_ingresos[0].container(border=True):
    "## Ganancias estimadas"
    f"### :green[${intereses_generados_no_morosos:,.{2}f}]"

with columnas_ingresos[1].container(border=True):
    "## Pérdidas estimadas"
    f"### :red[${-1*intereses_generados_morosos:,.{2}f}]"

with st.container(border=True):
    "## Neto estimado"
    neto = intereses_generados_no_morosos - intereses_generados_morosos
    st.write(f"### :{'green' if neto >= 0 else 'red'}[${neto:,.{2}f}]")

# Matriz de confusión para historial

grouped = np.array( df.groupby(["cb_person_default_on_file", "loan_status_cat"]).size().reset_index(name="count")["count"] ).reshape((2,2))

fig = plt.figure(figsize=(2, 2))
plt.imshow(grouped, interpolation='nearest')
plt.title('Matriz', fontsize=16)
plt.colorbar()
classes = ['Pagado a tiempo', 'Pagado con retraso']  # Cambiar según tus clases
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)
thresh = grouped.max() / 2.0
for i, j in np.ndindex(grouped.shape):
    plt.text(j, i, f'{grouped[i, j]}',
        horizontalalignment="center",
        color="white" if grouped[i, j] < thresh else "black")
plt.ylabel('Historial crediticio', fontsize=14)
plt.xlabel('Crédito actual', fontsize=14)
plt.tight_layout()
plt.show()

st.pyplot(fig,use_container_width=False)

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

# ==========================================
# Parte de Javier
# ==========================================

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
Q1 = df['person_income'].quantile(0.25)
Q3 = df['person_income'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

fig=px.bar(
    df[(df['person_income'] >= lower_bound) & (df['person_income'] <= upper_bound)].groupby(['person_income', "loan_status_cat"]).size().reset_index(name='count'),
    x="person_income",
    y="count",
    color="loan_status_cat",
    barmode="group",
    labels={'loan_status': 'Estado del crédito', 'count': 'Conteo', 'loan_intent': 'Intención de crédito'}
)
st.plotly_chart(fig)