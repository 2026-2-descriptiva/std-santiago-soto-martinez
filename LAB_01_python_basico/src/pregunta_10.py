import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Calcular la cantidad de elementos en la cuarta columna (índice 3) y la cantidad de pares en la quinta columna (índice 4)
    df['codes_count'] = df[3].str.split(',').apply(len)
    
    # Calcular la cantidad de pares en la quinta columna (índice 4) considerando que los pares están separados por comas
    df['metrics_count'] = df[4].str.split(',').apply(len)
    
    # Crear una lista de tuplas con la letra de la primera columna (índice 0), la cantidad de elementos de la cuarta columna y la cantidad de pares de la quinta columna
    resultado = list(zip(df[0], df['codes_count'], df['metrics_count']))
    
    # Retornar la lista de tuplas
    return resultado

if __name__ == "__main__":
    print(pregunta_10())