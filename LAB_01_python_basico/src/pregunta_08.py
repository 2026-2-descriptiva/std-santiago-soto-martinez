import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Agrupar por la segunda columna (índice 1) y construir la lista de letras correspondientes de la primera columna (índice 0), eliminando duplicados y ordenando alfabéticamente
    letras_por_valor = df.groupby(1)[0].apply(lambda x: sorted(set(x))).sort_index()
    
    # Convertir a lista de tuplas (valor, letras)
    return list(letras_por_valor.items())

if __name__ == "__main__":
    print(pregunta_08())