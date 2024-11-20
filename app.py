import streamlit as st

# IMPORANTE
# Este archivo es para configurar la navegación en el sitio web, usa "pages" para guardar archivos .py
# Y configura nuevas páginas en pages.toml

pages = [
    st.Page("pages/intro.py", title="Introducción"),
    st.Page("pages/datos.py", title="Visualización de datos"),
    st.Page("pages/visual.py", title="Gráficos"),
    st.Page("pages/formulario.py", title="Formulario"),
]

pg = st.navigation(pages)
pg.run()