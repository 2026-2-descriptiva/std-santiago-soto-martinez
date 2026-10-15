import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Encontrar el valor máximo y mínimo de la segunda columna (índice 1) para cada letra de la primera columna (índice 0) y ordenamiento alfabético
    max_min_por_letra = df.groupby(0)[1].agg(['max', 'min'])
    
    # Convertir a lista de tuplas (letra, máximo, mínimo)
    return list(max_min_por_letra.itertuples())     

if __name__ == "__main__":
    print(pregunta_05())