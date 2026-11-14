import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    
    #Calcula la retención de clientes por cohorte mensual a partir de
    #data/sales.csv.gz y genera en submission/ los archivos
    #cohort_retention.csv y cohort_retention_heatmap.png.
    
    raiz = Path(__file__).resolve().parent.parent
    arch = raiz / "data" / "sales.csv.gz"
    dir_salida = raiz / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(arch, usecols=["CustomerID", "OrderDate"])
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df = df.dropna(subset=["CustomerID", "OrderDate"])

    # Mes de cada compra y mes de la primera compra de cada cliente
    df["order_period"] = df["OrderDate"].dt.to_period("M")
    df["cohort_period"] = df.groupby("CustomerID")["order_period"].transform("min")
    df["period_index"] = (
        (df["order_period"].dt.year - df["cohort_period"].dt.year) * 12
        + (df["order_period"].dt.month - df["cohort_period"].dt.month)
    )

    # Clientes distintos activos por cohorte y período
    retention = (
        df.groupby(["cohort_period", "period_index"])["CustomerID"]
        .nunique()
        .rename("active_customers")
        .reset_index()
    )
    tamano = (
        retention[retention["period_index"] == 0]
        .set_index("cohort_period")["active_customers"]
        .rename("cohort_size")
    )
    retention = retention.join(tamano, on="cohort_period")
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )
    retention["cohort_month"] = retention["cohort_period"].astype(str)
    retention = (
        retention[["cohort_month", "period_index", "active_customers",
                   "cohort_size", "retention_rate"]]
        .sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)
    )
    retention.to_csv(dir_salida / "cohort_retention.csv", index=False)

    # --- Mapa de calor ---
    matriz = retention.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )
    # Períodos ya observables sin clientes activos = retención real de 0;
    # los que aún no ocurren (después del último mes de datos) quedan vacíos.
    ultimo = df["order_period"].max()
    for cohorte in matriz.index:
        p = pd.Period(cohorte, freq="M")
        max_periodo = (ultimo.year - p.year) * 12 + (ultimo.month - p.month)
        for j in matriz.columns:
            if j <= max_periodo and pd.isna(matriz.loc[cohorte, j]):
                matriz.loc[cohorte, j] = 0.0

    datos = np.ma.masked_invalid(matriz.values.astype(float))
    fig, ax = plt.subplots(
        figsize=(max(8, 0.9 * matriz.shape[1] + 3), max(5, 0.6 * matriz.shape[0] + 2))
    )
    cmap = plt.get_cmap("YlGnBu").copy()
    cmap.set_bad("white")
    im = ax.imshow(datos, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(matriz.shape[1]))
    ax.set_xticklabels(matriz.columns)
    ax.set_yticks(range(matriz.shape[0]))
    ax.set_yticklabels(matriz.index)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            v = matriz.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.0%}", ha="center", va="center",
                        color="white" if v > 0.6 else "black", fontsize=9)
    ax.set_xlabel("Período (meses desde la primera compra)")
    ax.set_ylabel("Cohorte (mes de la primera compra)")
    ax.set_title("Retención de clientes por cohorte")
    fig.colorbar(im, ax=ax, label="Tasa de retención")
    fig.tight_layout()
    fig.savefig(dir_salida / "cohort_retention_heatmap.png", dpi=150)
    plt.close(fig)

    return retention

if __name__ == "__main__":
   print(build_cohort_analysis())
