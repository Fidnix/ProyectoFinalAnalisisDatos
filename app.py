import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# IMPORANTE
# Este archivo es para configurar la navegación en el sitio web, usa "pages" para guardar archivos .py
# Y configura nuevas páginas en pages.toml

# st.set_page_config(layout="wide")
# nav = get_nav_from_toml("pages.toml")

# pg = st.navigation(nav)
# add_page_title(pg)
# pg.run()

pages = [
    st.Page("pages/intro.py", title="Introducción"),
    st.Page("pages/datos.py", title="Visualización de datos"),
    st.Page("pages/visual.py", title="Gráficos"),
    st.Page("pages/formulario.py", title="Formulario"),
]

pg = st.navigation(pages)
pg.run()