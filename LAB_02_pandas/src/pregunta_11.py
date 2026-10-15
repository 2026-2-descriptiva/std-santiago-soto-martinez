import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl1.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_11():
    """
    En `data/tbl1.tsv`, cada valor de la columna `c0` aparece en varias
    filas, una por cada letra de la columna `c4`. Construya un DataFrame con
    una fila por cada valor de `c0`, en orden ascendente, y las columnas `c0`
    y `c4`. En `c4`, escriba las letras de ese `c0` ordenadas alfabéticamente
    y separadas por comas.

    Ejemplo del formato de la respuesta:

            c0       c4
        0    0    b,f,g
        1    1    a,c,f
        2    2  a,c,e,f
        ...
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
    
    # Agrupar por `c0`, ordenar las letras de `c4` alfabéticamente y unirlas con comas
    df_agrupado = df.groupby("c0")["c4"].apply(lambda x: ",".join(sorted(x))).reset_index()
    
    # Ordenar por `c0` en orden ascendente
    df_agrupado = df_agrupado.sort_values("c0").reset_index(drop=True)
    
    # Retornar el DataFrame resultante
    return df_agrupado

if __name__ == "__main__":
    print(pregunta_11())
