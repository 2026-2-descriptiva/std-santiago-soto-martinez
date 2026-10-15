import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl0.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
    
    # Conteo de columnas en el DataFrame
    return(int(len(df.columns)))

if __name__ == "__main__":
    print(pregunta_02())
