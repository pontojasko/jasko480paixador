from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor
import subprocess
import sys
import re
import itertools

# Cores vibrantes para o efeito arco-íris
cores_rainbow = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
ciclo_cores = itertools.cycle(cores_rainbow)

# Worker para rodar o yt-dlp em segundo plano sem travar a UI
class DownloadThread(QThread):
    progresso = Signal(int)  # Envia a porcentagem real do download
    finalizado = Signal()  # Indica que o download terminou

    def __init__(self, comando):
        super().__init__()
        self.comando = comando

    def run(self):
        try:
            processo = subprocess.Popen(
                self.comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )

            for linha in processo.stdout:
                match = re.search(r'(\d+)%', linha)  # Captura progresso real do yt-dlp
                if match:
                    progresso = int(match.group(1))  # Converte para número inteiro
                    self.progresso.emit(progresso)  # Atualiza a barra de progresso

            processo.wait()
            self.progresso.emit(100)  # Garante que a barra finalize em 100%
            self.finalizado.emit()  # Dispara sinal de finalização

        except Exception as e:
            print(f"Erro no download: {e}")

# Interface principal
class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("baixador de mp3 480p do jasko")
        self.setGeometry(750, 400, 350, 100)
        
        layout = QVBoxLayout()

        # Fundo arco-íris animado
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_fundo)
        self.timer.start(300)

        self.label = QLabel("digitar o link do video")
        self.label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 30px; color: red;")
        layout.addWidget(self.label)

        self.entrada = QLineEdit()
        self.entrada.setStyleSheet("font-family: 'Comic Sans MS'; color:black; font-size: 20px; background-color: white;")
        layout.addWidget(self.entrada)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("QProgressBar { border: 3px solid black; text-align: center; font-family: 'Comic Sans MS'; font-size: 30px; } QProgressBar::chunk { background-color: lime; }")
        layout.addWidget(self.progress_bar)

        self.botao_mp480p = QPushButton("480p")
        self.botao_mp480p.setStyleSheet("background-color: blue; font-family: 'Comic Sans MS'; font-size: 20px;")
        self.botao_mp480p.clicked.connect(self.baixar_mp480p)
        layout.addWidget(self.botao_mp480p)

        self.botao_mp3 = QPushButton("mp3")
        self.botao_mp3.setStyleSheet("background-color: red; font-family: 'Comic Sans MS'; font-size: 20px;")
        self.botao_mp3.clicked.connect(self.baixar_mp3)
        layout.addWidget(self.botao_mp3)


        self.botao_mp4 = QPushButton("4k60fps")
        self.botao_mp4.setStyleSheet("background-color: black; color: orange; font-family: 'Comic Sans MS'; font-size: 8px;")
        self.botao_mp4.clicked.connect(self.baixar_mp4)
        layout.addWidget(self.botao_mp4)


        self.setLayout(layout)
        self.animar_fundo()
    
    def animar_fundo(self):
        cor_atual = next(ciclo_cores)
        self.setStyleSheet(f"background-color: {cor_atual};")
    
    def iniciar_download(self, comando):
        self.progress_bar.setValue(0)
        self.thread = DownloadThread(comando)
        self.thread.progresso.connect(self.progress_bar.setValue)
        self.thread.finalizado.connect(self.download_finalizado)
        self.thread.start()

    def baixar_mp3(self):
        url = self.entrada.text()
        if not url:
            QMessageBox.warning(self, "vish", "q porra de link eh esse?")
            return
        comando = f'yt-dlp -f bestaudio -x --audio-format mp3 --write-thumbnail --embed-thumbnail --embed-metadata "{url}"'
        self.iniciar_download(comando)

    def baixar_mp4(self):
        url = self.entrada.text()
        if not url:
            QMessageBox.warning(self, "vish", "q porra de link eh esse?")
            return
        comando = f'yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 --embed-metadata --embed-thumbnail --add-metadata "{url}"'
        self.iniciar_download(comando)

    def baixar_mp480p(self):
        url = self.entrada.text()
        if not url:
            QMessageBox.warning(self, "vish", "q porra de link eh esse?")
            return
        comando = f'yt-dlp -f "bestvideo[height<=480]+bestaudio[abr<=24]/best[height<=480]" --merge-output-format mp4 --audio-quality 24K --embed-metadata --embed-thumbnail --add-metadata "{url}"'
        self.iniciar_download(comando)

    def download_finalizado(self):
        print(f"baixou: {e}")

        

# Inicializando o aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = DownloaderApp()
    janela.show()
    sys.exit(app.exec())