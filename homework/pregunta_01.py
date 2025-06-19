# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |   | phrase                                                                                                                                                                 | target   |
    |--:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```
    """
    import zipfile
    import os
    import pandas as pd

    # Descomprimir el archivo zip principal que contiene los datos.
    with zipfile.ZipFile("files/input.zip", "r") as zip_ref:
        zip_ref.extractall(".")

    # Definir la ruta del directorio de salida según lo esperado por el test.
    output_dir = "files/output"
    
    # Crear el directorio 'files/output' si no existe.
    os.makedirs(output_dir, exist_ok=True)

    def generate_dataset(dataset_type, output_filename):
        """
        Función auxiliar para leer los archivos de una carpeta (train o test),
        procesarlos y generar el archivo CSV correspondiente.
        
        Args:
            dataset_type (str): El tipo de dataset a procesar ('train' o 'test').
            output_filename (str): La ruta del archivo CSV de salida.
        """
        data_records = []
        base_path = os.path.join("input", dataset_type)
        sentiments = ["positive", "negative", "neutral"]

        # Iterar sobre cada categoría de sentimiento.
        for sentiment in sentiments:
            sentiment_dir = os.path.join(base_path, sentiment)
            
            # Verificar que el directorio de sentimiento exista.
            if os.path.isdir(sentiment_dir):
                # Iterar sobre cada archivo de texto en el directorio.
                for filename in sorted(os.listdir(sentiment_dir)):
                    if filename.endswith(".txt"):
                        file_path = os.path.join(sentiment_dir, filename)
                        
                        # Leer el contenido del archivo (la frase).
                        with open(file_path, "r", encoding="utf-8") as f:
                            phrase = f.read().strip()
                        
                        # Agregar el registro a la lista con el nombre de columna 'target'.
                        data_records.append({"phrase": phrase, "target": sentiment})
        
        # Convertir la lista de registros a un DataFrame de pandas.
        df = pd.DataFrame(data_records)
        
        # Guardar el DataFrame como un archivo CSV.
        df.to_csv(output_filename, index=False)

    # Generar el dataset de entrenamiento.
    generate_dataset("train", os.path.join(output_dir, "train_dataset.csv"))
    
    # Generar el dataset de prueba.
    generate_dataset("test", os.path.join(output_dir, "test_dataset.csv"))