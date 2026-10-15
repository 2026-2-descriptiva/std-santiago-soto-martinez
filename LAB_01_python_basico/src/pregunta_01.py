import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Suma de la segunda columna (índice 1)
    return int(df.iloc[:, 1].sum())

if __name__ == "__main__":
    print(pregunta_01())
    