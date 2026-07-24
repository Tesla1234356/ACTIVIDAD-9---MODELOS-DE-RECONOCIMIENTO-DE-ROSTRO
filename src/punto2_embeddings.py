import os
import matplotlib.pyplot as plt
from deepface import DeepFace
from utils import setup_images

setup_images()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(base_dir, 'data', 'faces', 'img1.jpg')

print("Extrayendo vectores de características (Embeddings)...")
# Extraer embeddings (vectores) usando diferentes arquitecturas
# represent retorna una lista de diccionarios, tomamos el embedding del primer rostro
emb_facenet = DeepFace.represent(img_path=img_path, model_name='Facenet')[0]['embedding']
emb_vgg = DeepFace.represent(img_path=img_path, model_name='VGG-Face')[0]['embedding']

# Graficar los arreglos numéricos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
fig.suptitle("Punto 2: Vectores de Características (Embeddings)\nRepresentación matemática del rostro extraída por la red", fontsize=14)

ax1.plot(emb_facenet[:100], color='blue', marker='.') 
ax1.set_title(f"FaceNet Embedding (Mostrando 100 de {len(emb_facenet)} dimensiones)")
ax1.set_xlabel("Dimensión")
ax1.set_ylabel("Valor")
ax1.grid(True)

ax2.plot(emb_vgg[:100], color='orange', marker='.')
ax2.set_title(f"VGG-Face Embedding (Mostrando 100 de {len(emb_vgg)} dimensiones)")
ax2.set_xlabel("Dimensión")
ax2.set_ylabel("Valor")
ax2.grid(True)

plt.tight_layout()
plt.show()
