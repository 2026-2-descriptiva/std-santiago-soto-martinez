import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression='gzip', header=None, sep='\t')
    
    # Separar los pares `clave:valor` de la quinta columna (índice 4) y contar la cantidad de veces que aparece cada clave, ordenando alfabéticamente
    metrics_series = df[4].str.split(',', expand=True).stack()
    
    # Separar las claves y valores en columnas separadas
    metrics_df = metrics_series.str.split(':', expand=True)
    
    # Asignar nombres a las columnas
    metrics_df.columns = ['key', 'value']
    
    # Contar la cantidad de veces que aparece cada clave y ordenar alfabéticamente
    conteo_por_clave = metrics_df['key'].value_counts().sort_index()
    
    # Convertir a diccionario {clave: cantidad}
    return dict(conteo_por_clave)

if __name__ == "__main__":
    print(pregunta_09())