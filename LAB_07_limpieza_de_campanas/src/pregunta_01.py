import pandas as pd
from pathlib import Path


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    #Lee los diez archivos comprimidos de la campaña y los separa en las tablas
    #`client`, `campaign` y `economics`, guardadas en `submission/`.
    
    raiz = Path(__file__).resolve().parent.parent
    dir_datos = raiz / "data"
    dir_salida = raiz / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)

    # Lectura directa de los archivos comprimidos
    archivos = sorted(dir_datos.glob("bank-marketing-campaing-*.csv.gz"))
    assert archivos, "No se encontraron archivos de la campaña"
    df = pd.concat(
        [pd.read_csv(a, compression="gzip") for a in archivos],
        ignore_index=True,
    )
    # Se descarta la columna de índice que trae cada archivo
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df = df.drop_duplicates().sort_values("client_id").reset_index(drop=True)

    # --- client ---
    client = df[
        ["client_id", "age", "job", "marital", "education",
         "credit_default", "mortgage"]
    ].copy()
    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].mask(client["education"] == "unknown")
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # --- campaign ---
    campaign = df[
        ["client_id", "number_contacts", "contact_duration",
         "previous_campaign_contacts", "previous_outcome",
         "campaign_outcome"]
    ].copy()
    campaign["previous_outcome"] = (df["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (df["campaign_outcome"] == "yes").astype(int)
    fecha = pd.to_datetime(
        "2022-" + df["month"].str.lower() + "-" + df["day"].astype(str),
        format="%Y-%b-%d",
    )
    campaign["last_contact_date"] = fecha.dt.strftime("%Y-%m-%d")

    # --- economics ---
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # Escritura (CSV sin comprimir, sin índice)
    client.to_csv(dir_salida / "client.csv", index=False)
    campaign.to_csv(dir_salida / "campaign.csv", index=False)
    economics.to_csv(dir_salida / "economics.csv", index=False)

    return client, campaign, economics
  
if __name__ == "__main__":
    print(clean_campaign_data())

