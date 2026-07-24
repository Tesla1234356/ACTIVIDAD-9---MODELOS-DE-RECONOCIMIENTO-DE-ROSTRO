import os
import time
import matplotlib.pyplot as plt
from deepface import DeepFace
from utils import setup_images

setup_images()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img1_path = os.path.join(base_dir, 'data', 'faces', 'img1.jpg')
img2_path = os.path.join(base_dir, 'data', 'faces', 'img3.jpg')
db_path = os.path.join(base_dir, 'data', 'database')

# Warmup (cargar el modelo en memoria para que no afecte el primer tiempo)
print("Cargando modelos en memoria...")
DeepFace.build_model('VGG-Face')

# VERIFICACIÓN (1:1)
print("\n[1/2] Ejecutando Verificación (1:1)...")
start_time = time.time()
DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name='VGG-Face', enforce_detection=False)
verify_time = time.time() - start_time
print(f"Tiempo Verificación: {verify_time:.4f} segundos")

# RECONOCIMIENTO (1:N)
print("\n[2/2] Ejecutando Reconocimiento (1:N)...")
# Borrar caché previo si existe para una medición justa
pkl_path = os.path.join(db_path, "representations_vgg_face.pkl")
if os.path.exists(pkl_path):
    os.remove(pkl_path)

start_time = time.time()
# find() buscará la imagen en toda la carpeta db_path
DeepFace.find(img_path=img1_path, db_path=db_path, model_name='VGG-Face', enforce_detection=False, silent=True)
find_time = time.time() - start_time
print(f"Tiempo Reconocimiento: {find_time:.4f} segundos")

# Visualización Gráfica
labels = ['Verificación (1:1)\nSólo compara 2 fotos', f'Reconocimiento (1:N)\nBusca en base de datos']
times = [verify_time, find_time]

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, times, color=['#2ca02c', '#d62728'])
plt.title("Punto 3: Comparación de Tiempos\nVerificación Facial vs Reconocimiento Facial", fontsize=14)
plt.ylabel("Tiempo de ejecución (segundos)")

# Agregar los valores de texto encima de las barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.2f} s", ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylim(0, max(times) * 1.3) # Dar espacio arriba para el texto
plt.tight_layout()
plt.show()
