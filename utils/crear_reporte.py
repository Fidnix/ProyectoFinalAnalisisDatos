from fpdf import FPDF
import io
from PIL import Image

class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, "Reporte de resultados de crédito", align='C', ln=True)

    def add_section(self, title, x, y, w, h, content):
        # Dibujar el contenedor
        self.set_xy(x, y)
        self.set_fill_color(255, 255, 255)  # Fondo blanco
        self.rect(x, y, w, h, 'D')  # Dibujar rectángulo
        
        # Agregar título de la sección
        self.set_font('Arial', 'B', 12)
        self.set_xy(x + 2, y + 2)
        self.multi_cell(w - 4, 6, title)

        # Agregar contenido
        self.set_font('Arial', '', 10)
        self.set_xy(x + 2, y + 10)
        self.multi_cell(w - 4, 6, content)

    def add_image(self, image_path, x, y, w, h):
        self.image(image_path, x=x, y=y, w=w, h=h)

def crear_reporte(datos_aparte, datos_credito, estado_aprobado):
    pdf = CustomPDF()
    pdf.add_page()

    # Datos
    datos_personales = f"""
Nombre: {datos_aparte["nombre_cliente"]}
Edad: {datos_credito["person_age"]} años
Sueldo anual: s/. {datos_credito["person_income"]}
Tipo de residencia: {datos_credito["person_home_ownership"]}
Tiempo de trabajo: {datos_credito["person_emp_length"]} años
"""
    datos_credito2 = f"""
Intención del crédito: {datos_credito["loan_intent"]}
Grado de creditaje basado en el historial crediticio del solicitante: {datos_credito["loan_grade"]}
Cantidad de dinero solicitado: {datos_credito["loan_amnt"]}
El radio de interés asociado al crédito: 
Porcentaje de crédito respecto a ingreso:
"""
    historial_crediticio = f"""
...: {datos_credito["cb_person_default_on_file"]}
Ingrese total de años de actividad de créditos del individuo: {datos_credito["cb_person_cred_hist_length"]} año(s)
"""

    # Posiciones y dimensiones
    pdf.add_section("Datos personales", 10, 40, 190, 60, datos_personales)
    pdf.add_section("Datos de crédito", 10, 110, 190, 60, datos_credito2)
    pdf.add_section("Datos del historial crediticio", 10, 190, 190, 40, historial_crediticio)

    # Imagen de perfil
    pdf.image( Image.open(io.BytesIO(datos_aparte["imagen_cliente"])), x=130, y=50, w=40,h=40 )

    # Agregar contenedor de aprobación
    if estado_aprobado:
        pdf.set_fill_color(200, 255, 200)
    else:
        pdf.set_fill_color(255, 105, 97)
    pdf.set_xy(10, 160)
    pdf.rect(10, 250, 190, 20, 'FD')
    pdf.set_font('Arial', 'B', 12)

    if estado_aprobado:
        pdf.set_text_color(0, 128, 0)
    else:
        pdf.set_text_color(128, 0, 0)
    pdf.set_xy(10, 250)
    pdf.cell(180, 20, f"{'Fue' if estado_aprobado else 'No fue'} aprobado para el crédito", align='C')

    pdf_bytes = pdf.output(dest='S')
    pdf_buffer = io.BytesIO(pdf_bytes)

    return pdf_buffer

def crear_reporte_tabla(df):
    # Crear una instancia de FPDF
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Título del reporte
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(200, 10, txt="Reporte de Datos", ln=True, align="C")
    pdf.ln(10)
    
    # Encabezados de las columnas
    pdf.set_font("Arial", style="B", size=8)
    for columna in df.columns.tolist():
        pdf.cell(22, 10, txt=columna.replace("_", "\n").replace("person", "").replace("ownership", "").strip(), border=1, align="C")
    pdf.ln()
    
    # Contenido del DataFrame
    pdf.set_font("Arial", size=10)
    for _, fila in df.iterrows():
        for columna in df.columns.tolist():
            pdf.cell(22, 10, txt=str(fila[columna]), border=1, align="C")
        pdf.ln()
    
    # Guardar el PDF
    pdf_bytes = pdf.output(dest='S')
    pdf_buffer = io.BytesIO(pdf_bytes)

    return pdf_buffer
