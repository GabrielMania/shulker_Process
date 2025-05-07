import sys
import os
from PySide6 import QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDir
from compiler_base import CompilerBase
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QClipboard

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)

ui_file_path = os.path.join(os.path.dirname(__file__), "assemblerUi.ui")
window = loader.load(ui_file_path, None)

contador_bytes = int()
binario = str()
compiler = CompilerBase()
TEMP_FILE = os.path.join(os.path.dirname(__file__), "temp.sklanguage")

def converter():
    # Get the assembly code from the text box
    assembly_code = window.caixa_texto_assembly.toPlainText()
    
    # Save to temporary file
    with open(TEMP_FILE, 'w', encoding='utf-8') as f:
        f.write(assembly_code)
    
    # Compile the code
    success = compiler.convertdoc(TEMP_FILE)
    
    if success:
        # Read the output file
        output_path = os.path.join(os.path.dirname(__file__), "..", "output.skbin")
        with open(output_path, 'r', encoding='utf-8') as f:
            binary_output = f.read()
        
        # Update the binary text box
        window.caixa_texto_binario.setPlainText(binary_output)
        
        # Update byte counter
        byte_count = len(binary_output.strip().split('\n'))
        window.contador_bytes.setText(f"Bytes: {byte_count}")
    else:
        window.caixa_texto_binario.setPlainText("Erro na compilação")

def carregar():
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Assembly Files (*.sklanguage);;All Files (*)")
    if file_dialog.exec():
        filenames = file_dialog.selectedFiles()
        if filenames:
            try:
                with open(filenames[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                window.caixa_texto_assembly.setPlainText(content)
            except Exception as e:
                window.caixa_texto_assembly.setPlainText(f"Erro ao carregar arquivo: {str(e)}")

def copiar():
    clipboard = QtGui.QGuiApplication.clipboard()
    clipboard.setText(window.caixa_texto_binario.toPlainText())

def salvar():
    binary_content = window.caixa_texto_binario.toPlainText()
    if not binary_content:
        return
        
    file_dialog = QFileDialog()
    file_dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_dialog.setNameFilter("Binary Files (*.skbin);;All Files (*)")
    file_dialog.setDefaultSuffix("skbin")
    
    if file_dialog.exec():
        filenames = file_dialog.selectedFiles()
        if filenames:
            try:
                with open(filenames[0], 'w', encoding='utf-8') as f:
                    f.write(binary_content)
            except Exception as e:
                window.caixa_texto_binario.setPlainText(f"Erro ao salvar arquivo: {str(e)}")

def coletar_entrada():
    return window.caixa_texto_assembly.toPlainText()

def definir_saida(texto_saida):
    window.caixa_texto_binario.setPlainText(texto_saida)
    # Update byte counter
    byte_count = len(texto_saida.strip().split('\n'))
    window.contador_bytes.setText(f"Bytes: {byte_count}")

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