import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl0.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
    
    # Agrupar por la columna `c1`, ordenar los valores de `c2` y unirlos en un texto separado por `:`
    df_agrupado = df.groupby("c1")["c2"].apply(lambda x: ":".join(map(str, sorted(x)))).reset_index()
    
    # Renombrar la columna resultante a `c2`
    df_agrupado.columns = ["c1", "c2"]
    
    # Establecer la columna `c1` como índice y ordenar alfabéticamente
    df_agrupado.set_index("c1", inplace=True)
    
    # Retornar el DataFrame resultante
    return df_agrupado

if __name__ == "__main__":
    print(pregunta_10())
