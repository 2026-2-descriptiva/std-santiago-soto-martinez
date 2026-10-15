import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression="gzip", sep="\t", header=None)

    # Mes = caracteres 5 y 6 de "yyyy-mm-dd" (no valida que la fecha exista)
    meses = df[2].str[5:7]
    
    # Conteo de registros por mes y ordenamiento por mes
    conteo = meses.value_counts().sort_index()
    
    # Convertir a lista de tuplas (mes, cantidad) y retornar
    return list(conteo.items())

if __name__ == "__main__":
    print(pregunta_04())