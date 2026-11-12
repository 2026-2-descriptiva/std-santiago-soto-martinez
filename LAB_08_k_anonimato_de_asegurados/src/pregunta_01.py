import json
from pathlib import Path

import numpy as np
import pandas as pd

def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    """
    Mide el riesgo de reidentificación de data/insurance.csv.gz, evalúa dos
    esquemas de generalización y publica el que suprime menos registros.
    """
    K = 5
    raiz = Path(__file__).resolve().parent.parent
    arch_datos = raiz / "data" / "insurance.csv.gz"
    dir_salida = raiz / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(arch_datos)

    # --- Riesgo con los cuasi-identificadores originales ---
    qi_original = ["age", "sex", "bmi", "children", "region"]
    tam_original = df.groupby(qi_original)["age"].transform("size")
    original_k = int(tam_original.min())
    original_unique_records = int((tam_original == 1).sum())

    # --- Generalización ---
    df["age_group"] = pd.cut(
        df["age"], bins=[18, 30, 40, 50, 65], right=False,
        labels=["18-29", "30-39", "40-49", "50-64"],
    ).astype(str)
    df["bmi_group"] = pd.cut(
        df["bmi"], bins=[-np.inf, 18.5, 25, 30, np.inf], right=False,
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
    ).astype(str)
    df["children_group"] = np.select(
        [df["children"] == 0, df["children"].between(1, 2)],
        ["0", "1-2"],
        default="3+",
    )
    es_fumador = (df["smoker"] == "yes").astype(int)

    esquemas = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }

    resultados = {}
    publicados = {}
    for nombre, qi in esquemas.items():
        grupos = df.groupby(qi)
        tam = grupos["age"].transform("size")
        mantener = tam >= K          # se suprimen las clases con menos de K
        pub = df[mantener]

        # Diversidad del atributo sensible entre las clases publicadas
        fum = es_fumador[mantener]
        n_fum = fum.groupby([pub[c] for c in qi]).agg(["sum", "size"])
        sin_div = (n_fum["sum"] == 0) | (n_fum["sum"] == n_fum["size"])

        resultados[nombre] = {
            "quasi_identifiers": qi,
            "equivalence_classes": int(grupos.ngroups),
            "k_before_suppression": int(tam.min()),
            "suppressed_records": int((~mantener).sum()),
            "published_records": int(mantener.sum()),
            "published_classes": int(pub.groupby(qi).ngroups),
            "classes_without_smoker_diversity": int(sin_div.sum()),
            "records_without_smoker_diversity": int(n_fum.loc[sin_div, "size"].sum()),
        }
        publicados[nombre] = pub

    # Esquema que suprime menos registros (en empate, el primero)
    seleccionado = min(
        resultados, key=lambda n: resultados[n]["suppressed_records"]
    )
    pub_sel = publicados[seleccionado]

    reporte = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": resultados,
        "selected_scheme": seleccionado,
        "mean_charges_original": float(df["charges"].mean()),
        "mean_charges_published": float(pub_sel["charges"].mean()),
        "smoker_rate_original": float(es_fumador.mean()),
        "smoker_rate_published": float((pub_sel["smoker"] == "yes").mean()),
    }

    with open(dir_salida / "privacy_report.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    columnas = esquemas[seleccionado] + ["smoker", "charges"]
    pub_sel[columnas].to_csv(dir_salida / "insurance_published.csv", index=False)

    return reporte

if __name__ == "__main__":
    print(pregunta_01())
