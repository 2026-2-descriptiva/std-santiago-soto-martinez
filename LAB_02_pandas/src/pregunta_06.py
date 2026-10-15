import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "tbl1.tsv"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, sep = "\t")
    
    # Obtener los valores distintos de la columna `c4`, convertirlos a mayúsculas y ordenarlos alfabéticamente
    valores_distintos = df["c4"].str.upper().sort_values().unique()
    
    # Convertir a lista
    return list(valores_distintos)

if __name__ == "__main__":
    print(pregunta_06())
