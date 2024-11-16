import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# IMPORANTE
# Este archivo es para configurar la navegación en el sitio web, usa "pages" para guardar archivos .py
# Y configura nuevas páginas en pages.toml

st.set_page_config(layout="wide")
nav = get_nav_from_toml("pages.toml")

pg = st.navigation(nav)
add_page_title(pg)
pg.run()