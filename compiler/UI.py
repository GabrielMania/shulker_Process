import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader



loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window = loader.load("C:/Users/srgab/Desktop/assembler-1.0/assemblerUi.ui", None)



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


icone = QtGui.QIcon('C:/Users/srgab/Desktop/assembler-1.0/shulker.png')
window.setWindowTitle("SK2_assembler")
window.setWindowIcon(icone)
window.converter.clicked.connect(converter)
window.carregar.clicked.connect(carregar)
window.copiar.clicked.connect(copiar)
window.salvar.clicked.connect(salvar)
window.contador_bytes.setText(f"Bytes:{contador_bytes}")


window.show()
app.exec()