import os.path
import re
import pandas as pd

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    # Rutas y patrones para procesar el archivo de reporte
    ruta = (
        r"C:\Users\santi\OneDrive - Universidad Nacional de Colombia"
        r"\Documentos\Semestre 1\Descriptiva\std-santiago-soto-martinez"
        r"\LAB_03_ingestion_de_texto_plano\data\clusters_report.txt"
    )

    # Patrón para identificar el inicio de un clúster en el reporte
    patron_inicio = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s*(.*)$")

    # Lista para almacenar las filas del DataFrame y variable para el clúster actual
    filas = []
    actual = None

    # Leer el archivo línea por línea y extraer la información de cada clúster
    with open(ruta, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")

            coincidencia = patron_inicio.match(linea)
            if coincidencia:
                actual = {
                    "cluster": int(coincidencia.group(1)),
                    "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        coincidencia.group(3).replace(",", ".")
                    ),
                    "principales_palabras_clave": coincidencia.group(4).strip(),
                }
                filas.append(actual)
            elif actual and linea.strip() and not linea.strip().startswith("-"):
                # Línea de continuación de las palabras clave del clúster
                actual["principales_palabras_clave"] += " " + linea.strip()

    # Normalizar el texto de palabras clave
    for fila in filas:
        texto = re.sub(r"\s+", " ", fila["principales_palabras_clave"]).strip()
        texto = texto.rstrip(".")
        palabras = [p.strip() for p in texto.split(",") if p.strip()]
        fila["principales_palabras_clave"] = ", ".join(palabras)

    # Crear el DataFrame y retornarlo
    return pd.DataFrame(
        filas,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )
    
if __name__ == "__main__":
    print(pregunta_01())

