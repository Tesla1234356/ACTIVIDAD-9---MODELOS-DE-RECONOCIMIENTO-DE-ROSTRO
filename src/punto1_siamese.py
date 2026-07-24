import os
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
from utils import setup_images

# 1. Descargar imágenes si no existen
setup_images()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img1_path = os.path.join(base_dir, 'data', 'faces', 'img1.jpg')
img2_path = os.path.join(base_dir, 'data', 'faces', 'img3.jpg')

print("Calculando similitud con Red Siamesa (FaceNet)...")
# 2. Realizar la verificación (One-shot learning)
result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name='Facenet')

# 3. Mostrar resultado gráficamente
img1 = cv2.cvtColor(cv2.imread(img1_path), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(img2_path), cv2.COLOR_BGR2RGB)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Punto 1: One-Shot Learning (Verificación Facial)\nSimilitud calculada por Red Siamesa", fontsize=16)

axes[0].imshow(img1)
axes[0].set_title("Imagen 1 (Ancla)")
axes[0].axis('off')

axes[1].imshow(img2)
axes[1].set_title("Imagen 2 (Comparación)")
axes[1].axis('off')

match_text = "¡SON LA MISMA PERSONA!" if result['verified'] else "SON PERSONAS DISTINTAS"
color = 'green' if result['verified'] else 'red'
plt.figtext(0.5, 0.05, f"Resultado: {match_text}\nDistancia matemática: {result['distance']:.4f} (Umbral: {result['threshold']})", 
            ha="center", fontsize=14, bbox={"facecolor":color, "alpha":0.5, "pad":5})

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()
