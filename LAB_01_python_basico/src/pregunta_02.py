import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Conteo de registros por letra (columna 0) y ordenamiento alfabético
    conteo_por_letra = df[0].value_counts().sort_index()
    
    # Convertir a lista de tuplas (letra, cantidad)
    return list(conteo_por_letra.items())

if __name__ == "__main__":
    print(pregunta_02())