import pandas as pd
from utils.crear_reporte import crear_reporte_tabla

def test_tabla():
    df_salida = pd.read_csv("tests/prueba.csv")
    print(df_salida)
    buffer = crear_reporte_tabla(df_salida)
    with open("tests/resultado.pdf", "wb") as f:
        f.write(buffer.getvalue())