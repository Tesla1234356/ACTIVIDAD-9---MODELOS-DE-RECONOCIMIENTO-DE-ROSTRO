import cv2
import os
import glob
from deepface import DeepFace
import threading

# Variables Globales para permitir que los hilos compartan información
texto_estado = "Cargando..."
color = (255, 255, 0)
analizando = False

# Esta función correrá en el "fondo" sin interrumpir tu cámara
def analizar_rostro_en_fondo(frame_copy, db_dir):
    global texto_estado, color, analizando
    try:
        # Etapa 1: Anti-Spoofing
        faces = DeepFace.extract_faces(img_path=frame_copy, anti_spoofing=True, enforce_detection=False, detector_backend='opencv')
        
        if len(faces) > 0 and faces[0].get('confidence', 1.0) > 0.5:
            if not faces[0].get('is_real', True):
                texto_estado = "SPOOF / FOTO DETECTADA (Fraude)"
                color = (0, 0, 255)
            else:
                # Etapa 2: Reconocimiento (Cambié a 'Facenet' porque es más rápido que VGG-Face)
                dfs = DeepFace.find(img_path=frame_copy, db_path=db_dir, model_name='Facenet', enforce_detection=False, detector_backend='opencv', silent=True)
                
                if len(dfs) > 0 and not dfs[0].empty:
                    best_match = dfs[0].iloc[0]['identity']
                    name = os.path.basename(best_match).split('.')[0]
                    texto_estado = f"ASISTENCIA REGISTRADA: {name.upper()}"
                    color = (0, 255, 0)
                else:
                    texto_estado = "EMPLEADO DESCONOCIDO"
                    color = (0, 165, 255)
        else:
            # Si no hay cara clara, avisa
            texto_estado = "Buscando rostro claro..."
            color = (255, 255, 0)
    except Exception as e:
        pass
    
    # Liberamos el hilo para que se pueda analizar el siguiente cuadro
    analizando = False

def run_attendance_system():
    global texto_estado, color, analizando
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, 'data', 'database')
    os.makedirs(db_dir, exist_ok=True)

    print("="*60)
    print("SISTEMA DE ASISTENCIA (VERSIÓN MULTI-HILO ULTRA FLUIDA)")
    print("="*60)
    
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret: break
            
        # EFECTO ESPEJO (Voltear la cámara horizontalmente)
        frame = cv2.flip(frame, 1)
        
        fotos_en_db = glob.glob(os.path.join(db_dir, "*.jpg"))
        
        if len(fotos_en_db) == 0:
            texto_estado = "BASE DE DATOS VACIA. PRESIONA 'R' PARA REGISTRAR."
            color = (0, 255, 255)
        else:
            # === LA MAGIA DE LA FLUIDEZ (MULTI-THREADING) ===
            # Si no hay ningún análisis corriendo en el fondo, lanzamos uno.
            # Esto evita que la cámara se congele esperando a DeepFace.
            if not analizando:
                analizando = True
                
                # Truco 2: Achicamos la imagen un 50% antes de mandarla a IA para que la CPU no sufra
                frame_pequeno = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
                
                # Lanzar el hilo fantasma
                thread = threading.Thread(target=analizar_rostro_en_fondo, args=(frame_pequeno, db_dir))
                thread.daemon = True
                thread.start()

        # === DIBUJAR UI (Esto ahora corre a 30 FPS suaves como mantequilla) ===
        h, w, _ = frame.shape
        cv2.rectangle(frame, (10, 10), (w-10, h-10), color, 4)
        
        cv2.rectangle(frame, (15, 15), (w-15, 55), (0,0,0), -1)
        cv2.putText(frame, texto_estado, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.rectangle(frame, (15, h-45), (w-15, h-15), (0,0,0), -1)
        cv2.putText(frame, "[R] Registrar Trabajador | [Q] Salir", (20, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        
        cv2.imshow('Control de Asistencia (Multi-Hilo)', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            cv2.putText(frame, "MIRA LA TERMINAL (NEGRA) PARA ESCRIBIR TU NOMBRE", (30, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Control de Asistencia (Multi-Hilo)', frame)
            cv2.waitKey(1)
            
            nombre = input("\n📝 INGRESE EL NOMBRE: ")
            if nombre.strip():
                save_path = os.path.join(db_dir, f"{nombre.strip()}.jpg")
                cv2.imwrite(save_path, frame)
                print(f"✅ Trabajador registrado.")
                
                # Borrar caché (ojo, ahora es facenet)
                pkl_path = os.path.join(db_dir, "representations_facenet.pkl")
                if os.path.exists(pkl_path):
                    os.remove(pkl_path)
            
            # Forzamos reseteo del hilo al registrar
            analizando = False

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance_system()
