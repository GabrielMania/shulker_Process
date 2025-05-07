#ferramenta para criar sprites para uso no processador

# Importando Dependencias
import sys
import os
import contextlib
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

# Importando o conversor de PNG para binário
try:
    from conversor_png_bin import Conversor
except ImportError:
    # Tenta importar de caminho relativo
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from conversor_png_bin import Conversor

# Constantes globais
DEFAULT_GRID_SIZE = 8
MAX_GRID_SIZE = 128

# Paleta de cores suportadas
CORES = {
    "Preto": QtGui.QColor(8, 10, 15),      # Concreto Preto
    "Branco": QtGui.QColor(255, 255, 255), # Concreto Branco
    "Vermelho": QtGui.QColor(142, 33, 33), # Concreto Vermelho
    "Verde": QtGui.QColor(73, 91, 36),     # Concreto Verde
    "Azul": QtGui.QColor(45, 47, 143),     # Concreto Azul
    "Amarelo": QtGui.QColor(241, 175, 21), # Concreto Amarelo
    "Cinza": QtGui.QColor(55, 58, 62),     # Concreto Cinza
    "CinzaClaro": QtGui.QColor(125, 125, 115), # Concreto Cinza Claro
    "Marron": QtGui.QColor(96, 60, 32),    # Concreto Marrom
    "Laranja": QtGui.QColor(224, 97, 1),   # Concreto Laranja
    "VerdeClaro": QtGui.QColor(94, 169, 24), # Concreto Lima
    "Cyano": QtGui.QColor(21, 119, 136),   # Concreto Ciano
    "AzulClaro": QtGui.QColor(36, 137, 199), # Concreto Azul Claro
    "Roxo": QtGui.QColor(100, 32, 156),    # Concreto Roxo
    "Magenta": QtGui.QColor(169, 48, 159), # Concreto Magenta
    "Rosa": QtGui.QColor(213, 101, 143)    # Concreto Rosa
}

# Contexto para suprimir a saída padrão de erros
@contextlib.contextmanager
def suprimir_stderr():
    original = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stderr = original


class DrawingArea(QtWidgets.QWidget):
    """Área de desenho de sprites pixelados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = DEFAULT_GRID_SIZE
        self.current_color = Qt.black
        self.grid = [[Qt.white for _ in range(MAX_GRID_SIZE)] for _ in range(MAX_GRID_SIZE)]
        self.setMouseTracking(True)
        # Garantir proporção quadrada com tamanho mínimo
        self.setMinimumSize(200, 200)

    def paintEvent(self, event):
        """Desenha a grade de pixels na tela de forma proporcional com pixels quadrados"""
        painter = QtGui.QPainter(self)
        
        # Calcula o tamanho do pixel para manter proporção quadrada
        size = min(self.width(), self.height())
        pixel_size = size / self.grid_size
        
        # Calcula offsets para centralizar a grade na área disponível
        offset_x = (self.width() - (pixel_size * self.grid_size)) / 2
        offset_y = (self.height() - (pixel_size * self.grid_size)) / 2
        
        # Define a largura do contorno como 0 para eliminar espaços entre pixels
        pen = QtGui.QPen()
        pen.setWidth(0)
        painter.setPen(pen)
        
        # Desenha os pixels como quadrados perfeitos
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = offset_x + col * pixel_size
                y = offset_y + row * pixel_size
                rect = QtCore.QRectF(x, y, pixel_size, pixel_size)
                painter.fillRect(rect, self.grid[row][col])
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        """Manipula o evento de clique do mouse"""
        if event.button() == Qt.LeftButton:
            self.paint_cell(event.position())

    def mouseMoveEvent(self, event):
        """Manipula o evento de movimento do mouse"""
        if event.buttons() & Qt.LeftButton:
            self.paint_cell(event.position())

    def paint_cell(self, pos):
        """Pinta uma célula na posição indicada considerando o desenho proporcional"""
        # Calcula o tamanho do pixel para manter proporção quadrada
        size = min(self.width(), self.height())
        pixel_size = size / self.grid_size
        
        # Calcula offsets para centralizar a grade na área disponível
        offset_x = (self.width() - (pixel_size * self.grid_size)) / 2
        offset_y = (self.height() - (pixel_size * self.grid_size)) / 2
        
        # Ajusta as coordenadas com base nos offsets
        adjusted_x = pos.x() - offset_x
        adjusted_y = pos.y() - offset_y
        
        # Verifica se o clique está dentro da área de desenho
        if adjusted_x < 0 or adjusted_y < 0 or adjusted_x >= pixel_size * self.grid_size or adjusted_y >= pixel_size * self.grid_size:
            return
            
        # Calcula a célula baseada nas coordenadas ajustadas
        col = int(adjusted_x // pixel_size)
        row = int(adjusted_y // pixel_size)
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.grid[row][col] = self.current_color
            self.update()

    def set_grid_size(self, size):
        """Define o tamanho da grade"""
        self.grid_size = size
        # Mantenha os dados existentes ao redimensionar
        new_grid = [[Qt.white for _ in range(MAX_GRID_SIZE)] for _ in range(MAX_GRID_SIZE)]
        for row in range(min(size, len(self.grid))):
            for col in range(min(size, len(self.grid[0]))):
                new_grid[row][col] = self.grid[row][col]
        self.grid = new_grid
        self.update()

    def set_color(self, cor_nome):
        """Define a cor atual do pincel"""
        self.current_color = CORES.get(cor_nome, Qt.black)

    def clear_grid(self):
        """Limpa a grade"""
        self.grid = [[Qt.white for _ in range(MAX_GRID_SIZE)] for _ in range(MAX_GRID_SIZE)]
        self.update()

    def grid_to_binary(self):
        """Função vazia para compatibilidade"""
        # Função mantida vazia conforme solicitado
        return bytes()

    def binary_to_grid(self, data):
        """Função vazia para compatibilidade"""
        # Função mantida vazia conforme solicitado
        pass

    def grid_to_image(self):
        """Converte a grade para uma imagem"""
        image = QtGui.QImage(self.grid_size, self.grid_size, QtGui.QImage.Format_RGB32)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                image.setPixelColor(col, row, self.grid[row][col])
        return image

    def find_nearest_color(self, target_color):
        """Encontra a cor suportada mais próxima"""
        min_distance = float('inf')
        cor_mais_proxima = Qt.black
        
        # Converte o alvo para QColor se necessário
        if not isinstance(target_color, QtGui.QColor):
            target_color = QtGui.QColor(target_color)
        
        # Componentes RGB do alvo
        r1, g1, b1 = target_color.getRgb()[:3]
        
        for cor in CORES.values():
            # Converte para QColor caso necessário
            if not isinstance(cor, QtGui.QColor):
                cor = QtGui.QColor(cor)
            
            # Componentes RGB da cor candidata
            r2, g2, b2 = cor.getRgb()[:3]
            
            # Distância euclidiana no espaço RGB
            distancia = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
            
            if distancia < min_distance:
                min_distance = distancia
                cor_mais_proxima = cor
                
        return cor_mais_proxima

    def image_to_grid(self, image):
        """Converte uma imagem para a grade"""
        if image.isNull():
            return False
            
        scaled_image = image.scaled(self.grid_size, self.grid_size)
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = scaled_image.pixelColor(col, row)
                # Converte para a cor suportada mais próxima
                matched_color = self.find_nearest_color(color)
                self.grid[row][col] = matched_color
                
        self.update()
        return True


class SpriteEditor:
    """Classe principal do editor de sprites"""
    
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.load_ui()
        self.setup_ui()
        self.connect_signals()
        # Instancia o conversor
        self.conversor = Conversor()
        
    def load_ui(self):
        """Carrega a UI a partir do arquivo .ui"""
        loader = QUiLoader()
        ui_file_path = os.path.join(os.path.dirname(__file__), "HudSpriteEditor.ui")
        self.window = loader.load(ui_file_path, None)
        
        # Configura janela
        icon_path = os.path.join(os.path.dirname(__file__), "shulkerArtista.png")
        if os.path.exists(icon_path):
            icone = QtGui.QIcon(icon_path)
            self.window.setWindowIcon(icone)
        self.window.setWindowTitle("SKng_SpriteEditor")
        
    def setup_ui(self):
        """Configura os elementos da UI"""
        # Encontra elementos da UI
        self.areaDesenho = self.window.findChild(QtWidgets.QFrame, "areaDesenho")
        self.grid_combo = self.window.findChild(QtWidgets.QComboBox, "gridSizeComboBox")
        self.color_combo = self.window.findChild(QtWidgets.QComboBox, "comboBox")
        self.save_button = self.window.findChild(QtWidgets.QPushButton, "saveButton")
        self.load_button = self.window.findChild(QtWidgets.QPushButton, "loadButton")
        self.import_button = self.window.findChild(QtWidgets.QPushButton, "importButton")
        self.export_button = self.window.findChild(QtWidgets.QPushButton, "exportButton")
        
        # Configura área de desenho
        self.drawing_area = DrawingArea()
        layout = self.areaDesenho.layout()
        
        # Se não houver layout, cria um
        if not layout:
            layout = QtWidgets.QVBoxLayout(self.areaDesenho)
            layout.setContentsMargins(0, 0, 0, 0)
            self.areaDesenho.setLayout(layout)
            
        placeholder = self.window.findChild(QtWidgets.QWidget, "drawingAreaWidgetPlaceholder")
        if placeholder:
            layout.removeWidget(placeholder)
            placeholder.deleteLater()
            
        # Configura o widget para expandir em ambas as direções
        self.drawing_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Expanding
        )
        
        layout.addWidget(self.drawing_area)
        
        # Aplica configurações iniciais
        self.update_grid_size(self.grid_combo.currentText())
        self.update_color(self.color_combo.currentText())
        
    def connect_signals(self):
        """Conecta sinais dos controles às funções de callback"""
        self.grid_combo.currentTextChanged.connect(self.update_grid_size)
        self.color_combo.currentTextChanged.connect(self.update_color)
        self.save_button.clicked.connect(self.save_sprite)
        self.load_button.clicked.connect(self.load_sprite)
        self.import_button.clicked.connect(self.import_sprite)
        self.export_button.clicked.connect(self.export_sprite)
        
    def update_grid_size(self, text):
        """Atualiza o tamanho da grade"""
        try:
            size = int(text.split('x')[0])
            self.drawing_area.set_grid_size(size)
        except (ValueError, IndexError):
            QtWidgets.QMessageBox.warning(
                self.window, 
                "Erro", 
                f"Tamanho de grade inválido: {text}"
            )
            
    def update_color(self, color_name):
        """Atualiza a cor selecionada"""
        self.drawing_area.set_color(color_name)
        
    def save_sprite(self):
        """Salva o sprite como imagem"""
        file_name, filter_selected = QtWidgets.QFileDialog.getSaveFileName(
            self.window,
            "Salvar Sprite",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;Todos os Arquivos (*)"
        )
        
        if not file_name:
            return
            
        # Verifica se arquivo já existe
        if os.path.exists(file_name):
            confirma = QtWidgets.QMessageBox.question(
                self.window,
                "Confirmar Sobrescrever",
                f"O arquivo {os.path.basename(file_name)} já existe. Deseja sobrescrever?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirma == QtWidgets.QMessageBox.No:
                return
                
        image = self.drawing_area.grid_to_image()
        
        try:
            success = image.save(file_name)
            if not success:
                QtWidgets.QMessageBox.warning(
                    self.window, 
                    "Erro", 
                    f"Não foi possível salvar o arquivo {file_name}"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.window, 
                "Erro", 
                f"Erro ao salvar arquivo: {str(e)}"
            )
            
    def load_sprite(self):
        """Carrega um sprite de um arquivo de imagem"""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window,
            "Carregar Sprite",
            "",
            "Imagens (*.png *.jpg *.jpeg);;Todos os Arquivos (*)"
        )
        
        if not file_name:
            return
            
        with suprimir_stderr():
            image = QtGui.QImage(file_name)
            
        if image.isNull():
            QtWidgets.QMessageBox.warning(
                self.window, 
                "Erro", 
                f"Não foi possível carregar a imagem {file_name}"
            )
            return
            
        success = self.drawing_area.image_to_grid(image)
        if not success:
            QtWidgets.QMessageBox.warning(
                self.window, 
                "Erro", 
                "Erro ao converter imagem para o formato da grade"
            )
            
    def import_sprite(self):
        """Importa um sprite de um arquivo binário para a área de desenho"""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window,
            "Importar Sprite",
            "",
            "Sprite Binário (*.spbin *.scbin);;Todos os Arquivos (*)"
        )
        
        if not file_name:
            return
            
        # Usa o conversor para decodificar o arquivo binário
        try:
            imagem = self.conversor.decode(file_name)
            
            if imagem is None:
                QtWidgets.QMessageBox.warning(
                    self.window, 
                    "Erro", 
                    f"Não foi possível decodificar o arquivo {file_name}"
                )
                return
                
            # Ajusta o tamanho da grade baseado no tamanho da imagem
            if imagem.width() == 16 and imagem.height() == 16:
                # Encontra e seleciona o item 16x16 no combo box
                for i in range(self.grid_combo.count()):
                    if "16x16" in self.grid_combo.itemText(i):
                        self.grid_combo.setCurrentIndex(i)
                        break
            elif imagem.width() == 128 and imagem.height() == 128:
                # Encontra e seleciona o item 128x128 no combo box
                for i in range(self.grid_combo.count()):
                    if "128x128" in self.grid_combo.itemText(i):
                        self.grid_combo.setCurrentIndex(i)
                        break
                
            # Carrega a imagem na área de desenho
            success = self.drawing_area.image_to_grid(imagem)
            if not success:
                QtWidgets.QMessageBox.warning(
                    self.window, 
                    "Erro", 
                    "Erro ao converter imagem para o formato da grade"
                )
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.window, 
                "Erro", 
                f"Erro ao importar arquivo: {str(e)}"
            )
            
    def export_sprite(self):
        """Exporta a área de desenho para um arquivo binário"""
        # Determina a extensão baseada no tamanho da grade
        extensao = ".spbin" if self.drawing_area.grid_size <= 16 else ".scbin"
        
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.window,
            "Exportar Sprite",
            "",
            f"Sprite Binário (*{extensao});;Todos os Arquivos (*)"
        )
        
        if not file_name:
            return
            
        # Adiciona a extensão correta se não for especificada
        if not file_name.lower().endswith(extensao):
            file_name += extensao
            
        # Verifica se arquivo já existe
        if os.path.exists(file_name):
            confirma = QtWidgets.QMessageBox.question(
                self.window,
                "Confirmar Sobrescrever",
                f"O arquivo {os.path.basename(file_name)} já existe. Deseja sobrescrever?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirma == QtWidgets.QMessageBox.No:
                return
                
        try:
            # Converte a grade para uma imagem
            imagem = self.drawing_area.grid_to_image()
            
            # Usa o conversor para codificar a imagem
            success = self.conversor.encode(imagem, file_name)
            
            if not success:
                QtWidgets.QMessageBox.warning(
                    self.window, 
                    "Erro", 
                    f"Não foi possível exportar para {file_name}"
                )
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.window, 
                "Erro", 
                f"Erro ao exportar arquivo: {str(e)}"
            )
            
    def run(self):
        """Inicia a aplicação"""
        self.window.show()
        return self.app.exec()

# Execução principal
if __name__ == "__main__":
    editor = SpriteEditor()
    sys.exit(editor.run())