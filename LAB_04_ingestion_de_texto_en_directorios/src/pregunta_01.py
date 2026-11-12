import os.path
import pandas as pd
import time


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    # Rutas de las carpetas de entrenamiento y prueba
    train_dir = os.path.join("data", "train")
    test_dir = os.path.join("data", "test")

    # Función para construir el dataset a partir de una carpeta
    def construir_dataset(carpeta):
        frases = []
        targets = []
        for sentimiento in sorted(os.listdir(carpeta)):
            sentimiento_path = os.path.join(carpeta, sentimiento)
            if os.path.isdir(sentimiento_path):
                for archivo in sorted(os.listdir(sentimiento_path)):
                    if archivo.endswith(".txt"):
                        archivo_path = os.path.join(sentimiento_path, archivo)
                        with open(archivo_path, "r", encoding="utf-8") as f:
                            frase = f.read().strip()
                            frases.append(frase)
                            targets.append(sentimiento)
        return frases, targets

    # Construir datasets de entrenamiento y prueba
    train_frases, train_targets = construir_dataset(train_dir)
    test_frases, test_targets = construir_dataset(test_dir)

    # Crear DataFrames y guardarlos en CSV

    train_df = pd.DataFrame({"phrase": train_frases, "target": train_targets})
    test_df = pd.DataFrame({"phrase": test_frases, "target": test_targets})

    train_df.to_csv("submission/train_dataset.csv", index=False)
    test_df.to_csv("submission/test_dataset.csv", index=False)
    
if __name__ == "__main__":
    start_time = time.time()
    pregunta_01()
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
