# Trash Classifier Model Documentation

## Pasos realizados para crear el modelo

### 1. Descarga del dataset TrashNet
El dataset **TrashNet** fue descargado desde su fuente oficial. Este dataset contiene imágenes clasificadas en diferentes categorías de basura, como cartón, plástico, papel, metal, vidrio y desechos generales.

### 2. Redimensionamiento de las imágenes
Se utilizó el script [```resize.py```](scripts/resize.py) para redimensionar todas las imágenes del dataset a un tamaño uniforme de **256 x 256 píxeles**. Esto asegura que todas las imágenes tengan las mismas dimensiones, facilitando el procesamiento y entrenamiento del modelo.

### 3. Aumento del dataset
Para incrementar la cantidad de datos y mejorar la capacidad del modelo para generalizar, se utilizó el script [```augment.py```](scripts/augment.py). Este script generó **10 versiones aumentadas de cada imagen** aplicando transformaciones como:
- Alteración de brillo
- Modificación de contraste
- Desplazamiento
- Rotación
- Otros ajustes visuales

### 4. División del dataset
El dataset fue dividido en tres subconjuntos:
- **Train**: Para entrenar el modelo.
- **Validation (val)**: Para validar el rendimiento del modelo durante el entrenamiento.
- **Test**: Para evaluar el modelo final.  
Esta división se realizó utilizando un script que organizó las imágenes en carpetas específicas ([```train```](dataset/organized/train), [```val```](dataset/organized/val), [```test```](dataset/organized/test)).

### 5. Entrenamiento del modelo
El entrenamiento se llevó a cabo en **Google Colab** utilizando una GPU **NVIDIA L4** para acelerar el proceso. Se utilizó el notebook [```train.ipynb```](notebooks/train.ipynb), que incluye:
- La instalación de la librería **Ultralytics**.
- La carga del modelo YOLO preentrenado (`yolo11n-cls.pt`).
- El entrenamiento del modelo con los siguientes parámetros:
  - **Dataset**: Carpeta organizada con las imágenes (`./dataset/organized`).
  - **Épocas**: 100.
  - **Tamaño de imagen**: 256 px.
  - **Dispositivo**: GPU.

### 6. Pruebas del modelo
Se realizaron pruebas utilizando el subconjunto **test** del dataset mediante una interfaz gráfica desarrollada con **Streamlit**. Esta interfaz permite:
- Subir imágenes para realizar inferencias.
- Mostrar la clase predicha por el modelo.
- Visualizar las imágenes cargadas y los resultados de las predicciones.

Este flujo asegura un proceso completo desde la preparación de los datos hasta la evaluación del modelo en un entorno interactivo.

## Ejemplo de uso

<p align="center">
    <img src="https://i.postimg.cc/J02Pw6yY/Screenshot-171.png" alt="Prueba 1" width="600">
</p>

<p align="center">
    <img src="https://i.postimg.cc/Hk53KtT3/Screenshot-172.png" alt="Prueba 2" width="600">
</p>

<p align="center">
    <img src="https://i.postimg.cc/CMPvf1vC/Screenshot-173.png" alt="Prueba 3" width="600">
</p>

<p align="center">
    <img src="https://i.postimg.cc/kX2TNmZ0/Screenshot-174.png" alt="Prueba 4" width="600">
</p>

<p align="center">
    <img src="https://i.postimg.cc/15bJJd1f/Screenshot-175.png" alt="Prueba 5" width="600">
</p>

<p align="center">
    <img src="https://i.postimg.cc/MGSt8jTw/Screenshot-176.png" alt="Prueba 6" width="600">
</p>