import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "data.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    # Lectura del archivo (sin encabezado, separado por tabulaciones)
    df = pd.read_csv(ARCH_DATOS, compression="gzip", sep="\t", header=None)

    # Una fila por par: "jjj:12,bbb:3" -> filas "jjj:12" y "bbb:3"
    df["par"] = df[4].str.split(",")
    df = df.explode("par")

    # Quedarse con el número después de ":"
    df["numero"] = df["par"].str.split(":").str[1].astype(int)

    # Suma por letra, ordenada alfabéticamente
    sumas = df.groupby(0)["numero"].sum().sort_index()

    return {letra: int(suma) for letra, suma in sumas.items()}

if __name__ == "__main__":
    print(pregunta_12())