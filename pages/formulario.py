import streamlit as st
from utils.crear_reporte import crear_reporte
import numpy as np

# Modal para mostrar los resultados de la prediccion
@st.cache_data
def obtener_prediccion(datos_creditos):
    return np.random.randn() > 0.5

@st.dialog("Resultados de predicción")
def modal_prediccion(datos_aparte, datos_credito):
    st.title(datos_aparte["nombre_cliente"])
    st.image(
        datos_aparte["imagen_cliente"],
        width = 120
    )

    # Evaluacion por el modelo (Por cambiar)
    resultado_prediccion = obtener_prediccion(datos_credito)
    if resultado_prediccion:
        st.success("El cliente es apto para el crédito")
    else:
        st.error("El cliente no es apto para el crédito")
    
    pdf_bytes = crear_reporte(datos_aparte, datos_credito, resultado_prediccion)

    col_cerrar, col_imprimir = st.columns(2)
    with col_cerrar:
        if st.button("Cerrar", use_container_width=True):
            st.rerun()
    with col_imprimir:
        st.download_button(
            "Imprimir reporte",
            data=pdf_bytes,
            file_name=f"reporte-credito-{datos_aparte["nombre_cliente"]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        pass
datos_aparte = {
    "imagen_cliente": None,
}
datos_credito = {
    "loan_status": 0
}

with st.container(border=True):
    """
    # Formulario
    ---
    """
    # Nombre del cliente
    datos_aparte["nombre_cliente"] = st.text_input(
        "Escribe el nombre del cliente",
        placeholder="Ingrese el nombre",
        help="El nombre de quien solicita el crédito"
    )
    
    # Imagen del cliente
    col_nombre, col_img = st.columns(2)
    imagen_uploader = col_img.file_uploader(
        "Imagen del solicitante",
        type=["png", "jpg", "jpeg"]
    )
    if(imagen_uploader is not None):
        datos_aparte["imagen_cliente"] = imagen_uploader.read()
    default_profile_img = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"
    col_nombre.image(
        datos_aparte["imagen_cliente"] if(datos_aparte["imagen_cliente"] is not None) else default_profile_img,
        width = 120
    )

    # Columnas
    col_persona, col_hist_cred = st.columns(2, gap="large")
    with col_persona.container():
        # person_age
        datos_credito["person_age"] = st.number_input(
            "Ingrese la edad del cliente",
            min_value=18,
            max_value=140,
            value=18,
            placeholder="Ingrese la edad de la persona",
            help="La edad debe ser en años"
        )

        # person_income
        datos_credito["person_income"] = st.number_input(
            "Ingrese su ingreso anual (s/.) ",
            min_value=0.,
            max_value=10_000_000.0,
            value=1000.,
            format="%0.2f",
            placeholder="Ingrese el ingreso anual",
            help="Sobre el ingreso anual: "
        )

        # person_home_ownership
        opciones_resisdencias = {"RENT": "Rentado", "MORTAGE": "Hipotecado", "OWN": "Propio", "OTHER": "Otros"}
        datos_credito["person_home_ownership"] = st.selectbox(
            "Tipo de residencia ",
            opciones_resisdencias.keys(),
            index=3,
            format_func= lambda r: opciones_resisdencias[r],
            placeholder="Selecciona una residencia",
            help="Seleccione"
        )

        # person_emp_length
        datos_credito["person_emp_length"] = st.number_input(
            "Ingrese total de años de actividad laboral del individuo (años) ",
            min_value=0,
            max_value=140,
            value=1,
            placeholder="Ingrese el total de años que el invididuo trabaja",
            help="Sobre los años de actividad laboral: "
        )

    with col_hist_cred:
        # loan_intent
        opciones_intenciones = {
            "EDUCATION": "Educación",
            "MEDICAL": "Médido",
            "VENTURE": "Empresa",
            "PERSONAL": "Personal",
            "DEBTCONSOLIDATION": "Consolidación de débito",
            "HOMEIMPROVEMENT": "Mejora de hogar"
        }
        datos_credito["loan_intent"] = st.selectbox(
            "Intención del crédito ",
            opciones_intenciones.keys(),
            index=3,
            format_func= lambda r: opciones_intenciones[r],
            placeholder="Selecciona una intención de crédito",
            help="Seleccione"
        )

        # loan_grade
        # "Grado de creditaje basado en el historial crediticio del solicitante"
        opciones_grados = [chr(i) for i in range(65, 72)]
        datos_credito["loan_grade"] = st.selectbox(
            "Grado de creditaje basado en el historial crediticio del solicitante",
            opciones_grados,
            index=0,
            placeholder="Selecciona un grado de creditaje",
            help="Seleccione"
        )

        # loan_amnt
        # "Cantidad de dinero del crédito solicitado (En dólares)"
        datos_credito["loan_amnt"] = st.number_input(
            "Cantidad de dinero solicitado",
            min_value=100.,
            max_value=6_000_000.,
            value=250.,
            step=0.1,
            placeholder="Ingrese la cantidad solicitada en el préstamo",
            help="En dólares"
        )

        # loan_int_rate
        datos_credito["loan_int_rate"] = st.number_input(
            "Tasa de interés asociada al préstamo",
            min_value=0.,
            max_value=100.,
            value=6.,
            step=0.5,
            placeholder="Ingrese la tasa de interés asociado al crédito",
            help="Es un porcentaje"
        )

        # loan_percent_income
        "Porcentaje de crédito respecto a ingreso"

    with st.container():
        # cb_person_default_on_file
        datos_credito["cb_person_default_on_file"] = st.checkbox("El cliente tiene un historial de incumplimientos del solicitante según los registros de las agencias de crédito")
        # cb_person_cred_hist_length
        # "Longitud del historial crediticio del individuo"
        datos_credito["cb_person_cred_hist_length"] = st.number_input(
            "Longitud del historial crediticio del solicitante",
            min_value=0,
            max_value=100,
            value=1,
            placeholder="Ingrese el total de años del historial crediticio",
            help="Sobre los años del historial crediticio: "
        )
    if st.button("Enviar", use_container_width=True):
        if (
            len(datos_aparte["nombre_cliente"].strip()) == 0 or \
            datos_aparte["imagen_cliente"] is None
        ):
            st.error("Falta completar los datos del formulario")
        else:
            modal_prediccion(datos_aparte, datos_credito)
