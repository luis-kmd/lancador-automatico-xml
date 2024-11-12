import os
import sys
from PySide6.QtWidgets import QApplication, QFileDialog, QDialog, QProgressBar, QPlainTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, Signal, Slot
from main import processar_xmls
from program_ui import Ui_Dialog

# Configure o atributo antes de criar QApplication
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class WorkerThread(QThread):
    # Definindo sinais para progresso e texto
    progress = Signal(int, int)
    text_signal = Signal(str)
    finished = Signal

    def __init__(self, pasta_selecionada, pasta_lancadas, pasta_erros):
        super().__init__()
        self.pasta_selecionada = pasta_selecionada
        self.pasta_lancadas = pasta_lancadas
        self.pasta_erros = pasta_erros

    def run(self):
        def update_progress(current, total):
            self.progress.emit(current, total)  # Emite o sinal para atualizar a barra de progresso

        def update_text(texto):
            self.text_signal.emit(texto)  # Emite o sinal para atualizar o QPlainTextEdit

        processar_xmls(self.pasta_selecionada, self.pasta_lancadas, self.pasta_erros, update_progress, update_text)

class Lancador(QDialog):
    def __init__(self):
        super().__init__()  # Chamada correta ao construtor da classe base
        # Carregue o arquivo ui que foi transformado em py
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        
        self.show()
    
        # Definindo função dos botões
        self.botao_Selecionar = self.ui.SelecionarPasta
        self.botao_Lancar = self.ui.RealizarLancamento

        # Definindo logo
        self.setWindowIcon(QIcon("C:\\Users\\Luis Tvc\\Desktop\\MenuQT\\KMD.ico"))

        # Bloqueando botão antes de selecionar pasta
        self.botao_Lancar.setEnabled(False)

        # Definindo sinais
        self.botao_Selecionar.clicked.connect(self.selecionarPasta)
        self.botao_Lancar.clicked.connect(self.realizarLancamento)

        # Adicionando widgets
        self.barra_progresso = self.ui.BarraProgresso
        if self.barra_progresso is None:
            raise ValueError("Barra de progresso não encontrada. Verifique o nome do widget no arquivo .ui.")
        self.barra_progresso.setValue(0)
        
        self.plain_text_edit = self.ui.logdelancamento
        if self.plain_text_edit is None:
            raise ValueError("QPlainTextEdit não encontrado. Verifique o nome do widget no arquivo .ui.")
        self.plain_text_edit.setPlainText("")  # Inicialmente vazio

        self.barra_progresso.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgb(248, 230, 255);
                border-radius: 5px;
                text-align: center;
                background-color: #e6e6e6; /* cor do fundo da barra */
            }

            QProgressBar::chunk {
                background-color: #00FF00; /* cor preenchida da barra */
                border-radius: 5px; /* deixa o preenchimento arredondado */
                animation: progress-animation 1s ease-in-out infinite; /* animação suave */
            }
        """)

    def selecionarPasta(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta")
        if folder:
            print(f"Pasta selecionada: {folder}")
            self.pasta_selecionada = folder
            self.botao_Lancar.setEnabled(True)

    @Slot(int, int)
    def atualizar_barra_progresso(self, current, total):
        self.barra_progresso.setValue(int((current / total) * 100))

    @Slot(str)
    def atualizar_texto(self, texto):
        self.plain_text_edit.appendPlainText(texto)  # Atualiza o QPlainTextEdit

    def realizarLancamento(self):
        if not hasattr(self, 'pasta_selecionada') or not self.pasta_selecionada:
            print("Nenhuma pasta selecionada!")
            return
        
        pasta_lancadas = os.path.join(self.pasta_selecionada, 'lancadas')
        pasta_erros = os.path.join(self.pasta_selecionada, 'erros')

        # Cria e inicia a thread de trabalho
        self.thread = WorkerThread(self.pasta_selecionada, pasta_lancadas, pasta_erros)
        self.thread.progress.connect(self.atualizar_barra_progresso)  # Conecta o sinal de progresso ao slot de atualização
        self.thread.text_signal.connect(self.atualizar_texto)  # Conecta o sinal de texto ao slot de atualização
        self.thread.start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Lancador()
    sys.exit(app.exec())
    
