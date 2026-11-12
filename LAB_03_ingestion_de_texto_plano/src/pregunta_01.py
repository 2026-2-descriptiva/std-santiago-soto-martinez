import re
import pandas as pd
from pathlib import Path

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

    arch = Path(__file__).resolve().parent.parent / "data" / "clusters_report.txt"
    assert arch.exists()

    # Línea que inicia un clúster: número, cantidad, porcentaje y primer texto
    patron = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+(?:,\d+)?)\s*%\s*(.*)$")

    filas = []
    en_datos = False
    with open(arch, encoding="utf-8-sig") as f:
        for linea in f:
            linea = linea.rstrip("\r\n")
            # Los datos empiezan después de la línea de guiones
            if not en_datos:
                en_datos = linea.strip().startswith("---")
                continue
            if not linea.strip():
                continue
            m = patron.match(linea)
            if m:
                filas.append(
                    {
                        "cluster": int(m.group(1)),
                        "cantidad_de_palabras_clave": int(m.group(2)),
                        "porcentaje_de_palabras_clave": float(
                            m.group(3).replace(",", ".")
                        ),
                        "texto": m.group(4),
                    }
                )
            elif filas:
                # Línea de continuación de las palabras clave
                filas[-1]["texto"] += " " + linea

    # Normalización de las palabras clave de cada clúster
    for fila in filas:
        texto = re.sub(r"\s+", " ", fila["texto"]).strip().rstrip(".")
        palabras = [p.strip() for p in texto.split(",") if p.strip()]
        fila["principales_palabras_clave"] = ", ".join(palabras)
        del fila["texto"]

    return pd.DataFrame(filas)
    
if __name__ == "__main__":
    print(pregunta_01())

