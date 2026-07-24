# Actividad 09 - Modelos de Reconocimiento de Rostro (Visión Artificial)

Este repositorio contiene la implementación empírica y la resolución de la **Actividad 09**, centrada en el estado del arte de los algoritmos de reconocimiento facial, análisis arquitectónico de redes neuronales y detección *anti-spoofing*.

## 🚀 Arquitectura y Tecnologías
- **Core de IA:** [DeepFace](https://github.com/serengil/deepface) (Backend que orquesta FaceNet, VGG-Face y OpenFace).
- **Detección de Rostro (Landmarks):** MTCNN (Multi-task Cascaded Convolutional Networks), RetinaFace, OpenCV HAAR.
- **Implementación de Visión:** `cv2` (OpenCV).
- **Benchmarking y DataViz:** `matplotlib`, `time`, `pandas`.
- **Ejecución Asíncrona (Sistemas Embebidos):** Librería nativa `threading` de Python.

---

## 📂 Estructura del Proyecto

- `src/` - Códigos fuente con demostraciones.
  - `punto1_siamese.py` - Demostración de One-shot learning y validación de Redes Siamesas (Similitud del Coseno/L2).
  - `punto2_embeddings.py` - Extracción y visualización topológica de los vectores de características (Embeddings).
  - `punto3_speed.py` - Benchmarking comparativo de latencia: Verificación (1:1) vs Reconocimiento (1:N).
  - `punto4_detectors.py` - Comparativa de detectores: Modelos en Cascada (MTCNN) vs Single-Shot (RetinaFace/OpenCV).
  - `punto5_antispoofing.py` - Implementación base de evaluación de *Liveness* y mitigación de Deepfakes.
  - `punto5_realtime.py` & `sistema_asistencia.py` - Implementaciones funcionales en tiempo real utilizando la WebCam con arquitectura **Multi-Threading** para evitar *bottlenecks* de inferencia en sistemas embebidos.
- `data/` - Base de datos de rostros (`faces/`), archivos caché `.pkl` generados por los tensores de DeepFace y capturas de los resultados empíricos (`resultados/`).
- `Actividad 09.docx` - Instrucciones originales del requerimiento.
- `Informe_Final_Actividad_09.docx` - Informe técnico completo (generado con scripts Python) con fundamentación teórica de todas las validaciones.
- `requirements.txt` - Archivo para instalar todas las dependencias necesarias.

---

## ⚙️ Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Tesla1234356/ACTIVIDAD-9---MODELOS-DE-RECONOCIMIENTO-DE-ROSTRO.git
   cd "ACTIVIDAD-9---MODELOS-DE-RECONOCIMIENTO-DE-ROSTRO"
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecución:
   Navegar e inicializar cualquiera de los scripts de la carpeta `src/`, por ejemplo:
   ```bash
   python src/sistema_asistencia.py
   ```

## 🧠 Características Especiales
- **Seguridad Robusta:** Algoritmo que integra reconocimiento en tiempo real (FaceID) acoplado a un motor *Anti-Spoofing* (Liveness Score) que detecta micro-movimientos para prevenir ataques de fotos o pantallas.
- **Rendimiento SOTA (State of the Art):** Almacenamiento en caché de la representación matricial de los rostros y despliegue a través de múltiples hilos lógicos en procesadores locales.

---
*Desarrollado para la Unidad 2 del curso de Visión Artificial.*
