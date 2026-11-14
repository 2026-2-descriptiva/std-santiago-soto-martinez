import numpy as np
import pandas as pd
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """


    #Analiza la rentabilidad de data/superstore_orders.csv.gz y genera en
    #submission/ los archivos profitability_summary.csv, discount_summary.csv
    #y priority_segments.csv.
    
    raiz = Path(__file__).resolve().parent.parent
    arch = raiz / "data" / "superstore_orders.csv.gz"
    dir_salida = raiz / "submission"
    dir_salida.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(arch, sep=";", decimal=",", encoding="utf-8-sig")
    for c in ["Sales", "Profit", "Discount"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["loss"] = (-df["Profit"]).where(df["Profit"] < 0, 0.0)
    df["is_loss"] = (df["Profit"] < 0).astype(int)

    # Rango de descuento
    d = df["Discount"].round(6)
    df["discount_band"] = np.select(
        [d == 0, d <= 0.05, d <= 0.10],
        ["0%", "1%-5%", "6%-10%"],
        default="más de 10%",
    )

    def resumen(g):
        """Métricas de un grupo de líneas de pedido."""
        ventas = g["Sales"].sum()
        utilidad = g["Profit"].sum()
        return pd.Series(
            {
                "lines": len(g),
                "sales": ventas,
                "profit": utilidad,
                "profit_margin": utilidad / ventas if ventas else 0.0,
                "loss_lines": g["is_loss"].sum(),
                "loss_line_rate": g["is_loss"].mean() if len(g) else 0.0,
                "lost_profit": g["loss"].sum(),
            }
        )

    # 1. Resumen general
    general = resumen(df)
    general["orders"] = df["Order ID"].nunique()
    summary = pd.DataFrame([general])[
        ["lines", "orders", "sales", "profit", "profit_margin",
         "loss_lines", "loss_line_rate", "lost_profit"]
    ]
    for c in ["lines", "orders", "loss_lines"]:
        summary[c] = summary[c].astype(int)

    # 2. Resumen por rango de descuento (en el orden definido)
    bandas = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    filas = []
    for b in bandas:
        r = resumen(df[df["discount_band"] == b])
        r["discount_band"] = b
        filas.append(r)
    discount = pd.DataFrame(filas)[
        ["discount_band", "lines", "sales", "profit", "profit_margin",
         "loss_line_rate", "lost_profit"]
    ]
    discount["lines"] = discount["lines"].astype(int)

    # 3. Cinco segmentos segmento-categoría con mayor utilidad perdida
    claves = ["Customer Segment", "Product Category"]
    seg = pd.DataFrame(
        [
            {**dict(zip(claves, k)), **resumen(g).to_dict()}
            for k, g in df.groupby(claves)
        ]
    )
    seg = seg[seg["lines"] >= 100]
    priority = (
        seg.sort_values("lost_profit", ascending=False, kind="stable")
        .head(5)[claves + ["lines", "sales", "profit", "profit_margin", "lost_profit"]]
        .reset_index(drop=True)
    )
    priority["lines"] = priority["lines"].astype(int)

    # Redondeo a 4 decimales y escritura
    tablas = {
        "profitability_summary.csv": summary,
        "discount_summary.csv": discount,
        "priority_segments.csv": priority,
    }
    for nombre, t in tablas.items():
        cols = t.select_dtypes("float").columns
        t[cols] = t[cols].round(4)
        t.to_csv(dir_salida / nombre, index=False)

    return summary, discount, priority

if __name__ == "__main__":
    print(pregunta_01())