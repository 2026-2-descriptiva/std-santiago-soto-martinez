import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl0.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
    
    # Conteo de registros por categoría de la columna `c1` y ordenamiento alfabético
    conteo_por_categoria = df['c1'].value_counts().sort_index()
    
    # Retornar la Serie de Pandas con el conteo por categoría
    return conteo_por_categoria

if __name__ == "__main__":
    print(pregunta_03())
