import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Agrupar por la segunda columna (índice 1) y construir la lista de letras correspondientes de la primera columna (índice 0), conservando el orden y las repeticiones
    letras_por_valor = df.groupby(1)[0].apply(list).sort_index()
    
    # Convertir a lista de tuplas (valor, letras)
    return list(letras_por_valor.items())

if __name__ == "__main__":
    print(pregunta_07())