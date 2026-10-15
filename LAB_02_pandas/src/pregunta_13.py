import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS_TBL0 = DIR_DATOS / "tbl0.tsv"
ARCH_DATOS_TBL2 = DIR_DATOS / "tbl2.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS_TBL0.exists()
assert ARCH_DATOS_TBL2.exists()

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df0 = pd.read_csv(ARCH_DATOS_TBL0, sep = "\t")
    
    # Lectura del archivo `tbl2.tsv` (sin encabezado, separado por tabulaciones)
    df2 = pd.read_csv(ARCH_DATOS_TBL2, sep = "\t")
    
    # Combinar las tablas `tbl0` y `tbl2` usando la columna `c0`
    df_combinado = pd.merge(df0, df2, on="c0")
    
    # Sumar los valores de la columna `c5b` para cada categoría de la columna `c1` y ordenamiento alfabético
    suma_por_categoria = df_combinado.groupby("c1")["c5b"].sum().sort_index()
    
    # Convertir a Serie de Pandas
    return suma_por_categoria

if __name__ == "__main__":
    print(pregunta_13())
