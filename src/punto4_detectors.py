import os
import time
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
from utils import setup_images

setup_images()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(base_dir, 'data', 'faces', 'img1.jpg')
original_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

# Usamos opencv en lugar de mediapipe para evitar conflictos de instalación, 
# pero el concepto (One-shot vs Cascade) es el mismo con RetinaFace.
detectors = ['mtcnn', 'retinaface', 'opencv'] 
results = {}
times = {}

print("Detectando rostros con múltiples backends...")
for det in detectors:
    print(f"Probando {det}...")
    start_time = time.time()
    try:
        faces = DeepFace.extract_faces(img_path=img_path, detector_backend=det, enforce_detection=False)
        times[det] = time.time() - start_time
        if len(faces) > 0:
            results[det] = faces[0]['facial_area']
        else:
            results[det] = None
    except Exception as e:
        print(f"Error con {det}: {e}")
        times[det] = 0
        results[det] = None

# Visualización Gráfica
fig, axes = plt.subplots(1, len(detectors), figsize=(15, 5))
fig.suptitle("Punto 4: Detectores de Rostro\n(MTCNN: Cascada | RetinaFace/OpenCV: Single-Shot)", fontsize=16)

for ax, det in zip(axes, detectors):
    img_copy = original_img.copy()
    area = results.get(det)
    if area:
        # Dibujar un rectángulo verde donde se detectó el rostro
        cv2.rectangle(img_copy, (area['x'], area['y']), 
                      (area['x']+area['w'], area['y']+area['h']), (0, 255, 0), 3)
    
    ax.imshow(img_copy)
    time_taken = times.get(det, 0)
    ax.set_title(f"{det.upper()}\nTiempo: {time_taken:.3f} s", fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.show()
