import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Separar los pares clave:valor de la quinta columna y convertirlos en un DataFrame
    metrics_series = df[4].str.split(',', expand=True).stack()
    
    # Separar las claves y valores en columnas separadas
    metrics_df = metrics_series.str.split(':', expand=True)
    
    # Asignar nombres a las columnas y convertir los valores a enteros
    metrics_df.columns = ['key', 'value']
    
    # Convertir la columna 'value' a tipo entero
    metrics_df['value'] = metrics_df['value'].astype(int)
    
    # Agrupar por clave y calcular el valor mínimo y máximo, luego ordenar alfabéticamente
    min_max_por_clave = metrics_df.groupby('key')['value'].agg(['min', 'max']).sort_index()
    
    # Convertir a lista de tuplas (clave, mínimo, máximo)
    return list(min_max_por_clave.itertuples())
    

if __name__ == "__main__":
    print(pregunta_06())