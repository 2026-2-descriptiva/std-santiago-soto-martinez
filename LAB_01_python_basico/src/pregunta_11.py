import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression="gzip", sep="\t", header=None)

    # Una fila por letra: "b,g,f" -> tres filas con el mismo value
    df["letra"] = df[3].str.split(",")
    df = df.explode("letra")

    # Suma por letra, ordenada alfabéticamente
    sumas = df.groupby("letra")[1].sum().sort_index()

    return {letra: int(suma) for letra, suma in sumas.items()}

if __name__ == "__main__":
    print(pregunta_11())