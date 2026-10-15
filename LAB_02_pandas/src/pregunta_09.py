import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl0.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_09():
    """
    Retorne la tabla `data/tbl0.tsv` completa con una columna adicional
    llamada `year`, al final, que contenga el año de la fecha de la columna
    `c3` como un texto de cuatro caracteres.

    Ejemplo del formato de la respuesta:

            c0 c1  c2          c3  year
        0    0  E   1  1999-02-28  1999
        1    1  A   2  1999-10-28  1999
        2    2  B   5  1998-05-02  1998
        ...
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
