import sys
import os
from PySide6 import QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)

ui_file_path = os.path.join(os.path.dirname(__file__), "assemblerUi.ui")
window = loader.load(ui_file_path, None)

contador_bytes = int()
binario = str()

def converter():
    print('convertido')
    definir_saida(coletar_entrada())

def carregar():
    print('carregado')

def copiar():
    print("copiado")

def salvar():
    print("salvo")

def coletar_entrada():
    print("assembly coletado")
    texto_de_entrada = window.caixa_texto_assembly.toPlainText()
    return texto_de_entrada

def definir_saida(texto_saida):
    print("saida definida")
    window.caixa_texto_binario.setPlainText(texto_saida)

icon_path = os.path.join(os.path.dirname(__file__), "shulker.png")

icone = QtGui.QIcon(icon_path)
window.setWindowTitle("SK2_assembler")
window.setWindowIcon(icone)
window.converter.clicked.connect(converter)
window.carregar.clicked.connect(carregar)
window.copiar.clicked.connect(copiar)
window.salvar.clicked.connect(salvar)
window.contador_bytes.setText(f"Bytes:{contador_bytes}")

window.show()
app.exec()