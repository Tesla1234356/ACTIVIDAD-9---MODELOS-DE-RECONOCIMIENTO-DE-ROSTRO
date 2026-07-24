import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class RunScriptThread(QThread):
    output_signal = pyqtSignal(str)
    
    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path
        
    def run(self):
        self.output_signal.emit(f"Ejecutando: {os.path.basename(self.script_path)}...\n")
        self.output_signal.emit("Por favor espera, cargando modelos de IA...\n")
        
        # Ejecutar el script
        process = subprocess.Popen(
            [sys.executable, self.script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        for line in process.stdout:
            self.output_signal.emit(line)
            
        process.wait()
        self.output_signal.emit(f"\n--- Ejecución finalizada ---\n")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad 09 - Visión Artificial (Dashboard)")
        self.resize(850, 500)
        
        # Tema oscuro (Gozu mode)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: Consolas, monospace;
                font-size: 13px;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # --- PANEL IZQUIERDO (Botones) ---
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = QLabel("MENÚ PRINCIPAL\nModelos Faciales")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title)
        left_layout.addSpacing(20)
        
        # Lista de scripts
        btn_data = [
            ("Punto 1: One-Shot & Siamesas", "punto1_siamese.py"),
            ("Punto 2: Vectores (Embeddings)", "punto2_embeddings.py"),
            ("Punto 3: Verificación vs Reconoc. (Velocidad)", "punto3_speed.py"),
            ("Punto 4: Detectores (MTCNN/Retina)", "punto4_detectors.py"),
            ("Punto 5: Anti-Spoofing (Deepfakes)", "punto5_antispoofing.py")
        ]
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        for text, script in btn_data:
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            # El lambda requiere enlazar el valor actual de script
            btn.clicked.connect(lambda checked, s=script: self.run_script(s))
            left_layout.addWidget(btn)
            
        left_layout.addSpacing(20)
        
        btn_setup = QPushButton("1° Descargar Imágenes (Requerido)")
        btn_setup.setStyleSheet("background-color: #198754; margin-top: 20px;")
        btn_setup.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_setup.clicked.connect(lambda: self.run_script("utils.py"))
        left_layout.addWidget(btn_setup)
        
        # --- PANEL DERECHO (Consola) ---
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        
        console_title = QLabel("Terminal de Salida y Estado:")
        console_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(console_title)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setText("¡Bienvenido al Panel de Control de Visión Artificial!\n\n1. Primero haz clic en 'Descargar Imágenes'.\n2. Luego haz clic en cualquier Punto para ejecutar el código.\n3. Aparecerá una ventana gráfica con los resultados de cada análisis.")
        right_layout.addWidget(self.console)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
        self.thread = None

    def run_script(self, script_name):
        script_path = os.path.join(self.base_dir, script_name)
        if not os.path.exists(script_path):
            self.console.append(f"\nError: No se encuentra {script_path}")
            return
            
        self.console.append(f"\n{'='*50}\nIniciando {script_name}...\n{'='*50}")
        
        self.thread = RunScriptThread(script_path)
        self.thread.output_signal.connect(self.update_console)
        self.thread.start()

    def update_console(self, text):
        self.console.insertPlainText(text)
        # Auto-scroll al final
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
