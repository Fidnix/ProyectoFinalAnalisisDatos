import streamlit as st

# Inicialización de datos de sesión
if "numero_datos" not in st.session_state:
    st.session_state.numero_datos = 10_000
if "full_dataset" not in st.session_state:
    st.session_state.full_dataset = False
if "outliers" not in st.session_state:
    st.session_state.outliers = True

# Navegación
pages = [
    st.Page("pages/principal.py", title="Gráficos principales", default=True, icon="📊"),
    st.Page("pages/formulario.py", title="Formulario", icon="📃"),
    st.Page("pages/intro.py", title="Integrantes", icon="🧑"),
]

pg = st.navigation(pages)
pg.run()