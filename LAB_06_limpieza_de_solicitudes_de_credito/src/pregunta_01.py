import json
import re
import pandas as pd
from pathlib import Path

# Rutas
DIR_DATOS = Path(__file__).resolve().parent.parent / "data"
ARCH_DATOS = DIR_DATOS / "solicitudes_de_credito.csv.gz"

# Existencia de dicha ruta
assert ARCH_DATOS.exists()

def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    
    #Limpia data/solicitudes_de_credito.csv.gz y guarda el resultado en
    #submission/solicitudes_de_credito.csv (separador ';', sin índice).
    
    columnas = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "estrato", "comuna_ciudadano", "fecha_de_beneficio",
        "monto_del_credito", "línea_credito",
    ]
    texto = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "línea_credito",
    ]

    # Lectura como texto (el archivo usa ';') y descarte del índice
    df = pd.read_csv(
        ARCH_DATOS, sep=";", dtype=str, keep_default_na=False, encoding="utf-8"
    )
    df.columns = [c.strip() for c in df.columns]
    df = df[columnas].copy()

    # Campos de texto: minúsculas, guiones/guiones bajos como espacios,
    # espacios múltiples colapsados y sin espacios en los extremos
    for c in texto:
        df[c] = (
            df[c]
            .str.lower()
            .str.replace(r"[-_]", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Valores faltantes: vacíos o marcas de nulo -> NA
    for c in columnas:
        limpio = df[c].str.strip()
        df[c] = limpio.mask(limpio.str.lower().isin(["", "n/a", "na", "nan", "none"]))

    # Fechas: AAAA/MM/DD o D/MM/AAAA -> AAAA-MM-DD
    f = df["fecha_de_beneficio"]
    iso = f.str.match(r"^\d{4}/")
    fechas = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    fechas[iso] = pd.to_datetime(f[iso], format="%Y/%m/%d", errors="coerce")
    fechas[~iso] = pd.to_datetime(f[~iso], format="%d/%m/%Y", errors="coerce")
    df["fecha_de_beneficio"] = fechas.dt.strftime("%Y-%m-%d")

    # Monto: quitar símbolo, separador de miles y decimales ('$ 1,200,000.00')
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace(r"[\$\s,]", "", regex=True)
        .str.replace(r"\.0+$", "", regex=True)
    )

    # Registros incompletos (comuna_ciudadano puede quedar vacía)
    obligatorias = [c for c in columnas if c != "comuna_ciudadano"]
    df = df.dropna(subset=obligatorias)

    # Estrato y monto como enteros
    df["estrato"] = pd.to_numeric(df["estrato"]).astype(int)
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"]).astype(int)

    # Duplicados
    df = df.drop_duplicates().reset_index(drop=True)

    # Escritura
    dir_salida = Path(__file__).resolve().parent.parent / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)
    df.to_csv(dir_salida / "solicitudes_de_credito.csv", sep=";", index=False)

    return df


if __name__ == "__main__":
    print(pregunta_01().shape)
