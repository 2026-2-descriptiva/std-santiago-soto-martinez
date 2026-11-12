import json
import re
import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "ventas.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    
    # Construye el reporte de calidad de data/ventas.csv.gz.
    columnas_requeridas = [
        "supplier_id", "supplier", "country", "city", "purchase_date",
        "amount", "discount", "weight", "units", "unit_price", "contact_email",
    ]
    regex_email = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    # Se lee todo como texto, sin convertir nulos, para no alterar los valores
    df = pd.read_csv(
        ARCH_DATOS,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        encoding="utf-8-sig",
    )

    # Normalización de encabezados
    df.columns = [
        c.replace("\ufeff", "").strip().lower().replace(" ", "_")
        for c in df.columns
    ]
    columnas = list(df.columns)

    # Columnas requeridas / inesperadas
    faltantes_req = sorted(set(columnas_requeridas) - set(columnas))
    inesperadas = sorted(set(columnas) - set(columnas_requeridas))

    # Duplicados
    duplicate_row_count = int(df.duplicated().sum())
    if "supplier_id" in df.columns:
        duplicate_supplier_id_row_count = int(
            df["supplier_id"].duplicated(keep=False).sum()
        )
    else:
        duplicate_supplier_id_row_count = 0

    # Valores faltantes por columna (vacío, solo espacios o 'N/A')
    missing_by_col = {}
    for c in columnas:
        limpio = df[c].str.strip()
        missing_by_col[c] = int(((limpio == "") | (limpio.str.upper() == "N/A")).sum())

    # Correos inválidos
    if "contact_email" in df.columns:
        invalid_email_count = int(
            (~df["contact_email"].str.match(regex_email)).sum()
        )
    else:
        invalid_email_count = 0

    # Unidades inválidas: numéricas que no son enteros positivos
    invalid_unit_count = 0
    if "units" in df.columns:
        limpio = df["units"].str.strip()
        no_faltante = ~((limpio == "") | (limpio.str.upper() == "N/A"))
        nums = pd.to_numeric(df.loc[no_faltante, "units"], errors="coerce").dropna()
        invalid_unit_count = int(((nums <= 0) | (nums % 1 != 0)).sum())

    # Valores distintos de country, tal como aparecen
    if "country" in df.columns:
        country_values = sorted(df["country"].unique().tolist())
    else:
        country_values = []

    reporte = {
        "row_count": int(len(df)),
        "column_count": int(len(columnas)),
        "missing_required_columns": faltantes_req,
        "unexpected_columns": inesperadas,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_by_col,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    # Escritura del reporte
    dir_salida = Path(__file__).resolve().parent.parent / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)
    with open(dir_salida / "data_quality_report.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    return reporte


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))