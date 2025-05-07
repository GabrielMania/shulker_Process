"""
Conversor de imagens PNG para formatos binários textuais
- spbin: formato para imagens até 16x16 (4bits X + 4bits Y + 4bits fixos + 4bits cor)
- scbin: formato para imagens 128x128 (4bits cor + 12bits não usados)
"""

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
import os
import sys

# Paleta de cores suportadas - deve ser igual à do shinp.py
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

class Conversor:
    """Classe para conversão entre imagens PNG e formatos binários textuais"""
    
    def __init__(self):
        # Cor de transparência/fundo que não será codificada nos arquivos spbin
        self.cor_transparente = Qt.white
        # Lista de cores disponíveis para facilitar a busca de índices
        self.lista_cores = list(CORES.values())
    
    def espelhar_binario(self, binario):
        """
        Espelha apenas a significância dos bits (mais significativo à direita)
        Exemplo: 1011 (11 decimal) se torna 1101 (13 decimal) porque:
        1011 = 8+0+2+1 = 11
        1101 = 8+4+0+1 = 13
        """
        resultado = ""
        for bit in binario:
            resultado = bit + resultado
        return resultado
    
    def encontrar_indice_cor(self, cor):
        """Encontra o índice da cor na paleta, com tolerância"""
        if not isinstance(cor, QtGui.QColor):
            cor = QtGui.QColor(cor)

        # Componentes RGB da cor alvo
        r1, g1, b1 = cor.getRgb()[:3]
        
        # Se a transparência for maior que 128, considere como transparente
        if cor.alpha() < 128:
            return self.lista_cores.index(self.cor_transparente)
        
        # Encontra a cor mais próxima
        min_distance = float('inf')
        indice_cor_proxima = 0
        
        for i, cor_paleta in enumerate(self.lista_cores):
            if not isinstance(cor_paleta, QtGui.QColor):
                cor_paleta = QtGui.QColor(cor_paleta)
                
            r2, g2, b2 = cor_paleta.getRgb()[:3]
            distancia = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
            
            if distancia < min_distance:
                min_distance = distancia
                indice_cor_proxima = i
                
        return indice_cor_proxima
    
    def encode(self, imagem, arquivo_saida):
        """
        Codifica uma imagem em formato binário textual
        
        Args:
            imagem: Objeto QImage ou caminho para imagem PNG
            arquivo_saida: Caminho para salvar o arquivo binário
        
        Returns:
            bool: True se sucesso, False se erro
        """
        # Carrega a imagem se for um caminho
        if isinstance(imagem, str):
            img = QtGui.QImage(imagem)
            if img.isNull():
                return False
        else:
            img = imagem
            
        # Determina o formato baseado no tamanho
        largura = img.width()
        altura = img.height()
        
        if largura <= 16 and altura <= 16:
            # Formato SPBIN (até 16x16)
            return self._encode_spbin(img, arquivo_saida)
        elif largura == 128 and altura == 128:
            # Formato SCBIN (128x128)
            return self._encode_scbin(img, arquivo_saida)
        else:
            # Tamanho não suportado
            return False
    
    def _encode_spbin(self, img, arquivo_saida):
        """Codifica imagem no formato SPBIN (até 16x16)"""
        try:
            linhas = []
            
            # Para cada pixel não-transparente
            for y in range(img.height()):
                for x in range(img.width()):
                    cor = img.pixelColor(x, y)
                    
                    # Pula pixels com a cor transparente
                    if self._cor_igual(cor, self.cor_transparente):
                        continue
                    
                    # Encontra o índice da cor na paleta
                    indice_cor = self.encontrar_indice_cor(cor)
                    
                    # Codifica as coordenadas X, Y e a cor em 16 bits
                    # Mantém formato xxxxyyyy0000cccc
                    x_bin = format(x, '04b')       # 4 bits para X (0-15)
                    y_bin = format(y, '04b')       # 4 bits para Y (0-15)
                    fixo = '0000'                  # 4 bits fixos
                    cor_bin = format(indice_cor, '04b')  # 4 bits para cor
                    
                    # Monta o binário no formato correto e depois espelha cada bit
                    binario_completo = x_bin + y_bin + fixo + cor_bin
                    binario_espelhado = self.espelhar_binario(binario_completo)
                    
                    linhas.append(binario_espelhado + '\n')
            
            # Adiciona o marcador de finalização (espelhado)
            marcador_final = '0000000011110000'
            marcador_espelhado = self.espelhar_binario(marcador_final)
            linhas.append(marcador_espelhado + '\n')
            
            # Escreve no arquivo
            with open(arquivo_saida, 'w') as f:
                f.writelines(linhas)
                
            return True
            
        except Exception as e:
            print(f"Erro ao codificar SPBIN: {str(e)}")
            return False
    
    def _encode_scbin(self, img, arquivo_saida):
        """Codifica imagem no formato SCBIN (128x128)"""
        try:
            linhas = []
            
            # Para cada pixel
            for y in range(img.height()):
                for x in range(img.width()):
                    cor = img.pixelColor(x, y)
                    
                    # Encontra o índice da cor na paleta
                    indice_cor = self.encontrar_indice_cor(cor)
                    
                    # Codifica no formato cccc000000000000
                    cor_bin = format(indice_cor, '04b')
                    zeros = '0' * 12
                    
                    # Monta o binário e espelha cada bit
                    binario_completo = cor_bin + zeros
                    binario_espelhado = self.espelhar_binario(binario_completo)
                    
                    linhas.append(binario_espelhado + '\n')
            
            # Adiciona o marcador de finalização (espelhado)
            marcador_final = '1111111111111111'
            marcador_espelhado = self.espelhar_binario(marcador_final)
            linhas.append(marcador_espelhado + '\n')
            
            # Escreve no arquivo
            with open(arquivo_saida, 'w') as f:
                f.writelines(linhas)
                
            return True
            
        except Exception as e:
            print(f"Erro ao codificar SCBIN: {str(e)}")
            return False
    
    def decode(self, arquivo_entrada):
        """
        Decodifica um arquivo binário textual em uma imagem
        
        Args:
            arquivo_entrada: Caminho para o arquivo binário
        
        Returns:
            QImage: Imagem decodificada ou None se erro
        """
        try:
            # Verifica a extensão para determinar o formato
            _, ext = os.path.splitext(arquivo_entrada)
            ext = ext.lower()
            
            if ext == '.spbin':
                return self._decode_spbin(arquivo_entrada)
            elif ext == '.scbin':
                return self._decode_scbin(arquivo_entrada)
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao decodificar: {str(e)}")
            return None
    
    def _decode_spbin(self, arquivo_entrada):
        """Decodifica arquivo SPBIN (até 16x16)"""
        try:
            # Lê as linhas do arquivo
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
            
            if not linhas:
                return None
            
            # Cria uma imagem 16x16 transparente
            imagem = QtGui.QImage(16, 16, QtGui.QImage.Format_RGBA8888)
            imagem.fill(QtGui.QColor(255, 255, 255, 255))  # Branco
            
            # Para cada linha (exceto a última que é o marcador de finalização)
            for i in range(len(linhas) - 1):
                binario_espelhado = linhas[i].strip()
                
                # Valida o formato
                if len(binario_espelhado) != 16:
                    continue
                
                # Desfaz o espelhamento
                binario = self.espelhar_binario(binario_espelhado)
                
                # Extrai as informações no formato xxxxyyyy0000cccc
                x_bin = binario[:4]
                y_bin = binario[4:8]
                # Bits 8-11 são fixos em 0000
                cor_bin = binario[12:16]
                
                x = int(x_bin, 2)
                y = int(y_bin, 2)
                indice_cor = int(cor_bin, 2)
                
                # Verifica limites
                if x >= 16 or y >= 16 or indice_cor >= len(self.lista_cores):
                    continue
                
                # Define a cor do pixel
                cor = self.lista_cores[indice_cor]
                if not isinstance(cor, QtGui.QColor):
                    cor = QtGui.QColor(cor)
                
                imagem.setPixelColor(x, y, cor)
            
            return imagem
            
        except Exception as e:
            print(f"Erro ao decodificar SPBIN: {str(e)}")
            return None
    
    def _decode_scbin(self, arquivo_entrada):
        """Decodifica arquivo SCBIN (128x128)"""
        try:
            # Lê as linhas do arquivo
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
            
            if not linhas:
                return None
            
            # Cria uma imagem 128x128
            imagem = QtGui.QImage(128, 128, QtGui.QImage.Format_RGB32)
            imagem.fill(QtGui.QColor(255, 255, 255))  # Branco como padrão
            
            # Para cada linha (exceto a última que é o marcador de finalização)
            for i in range(min(len(linhas) - 1, 128 * 128)):
                binario_espelhado = linhas[i].strip()
                
                # Valida o formato
                if len(binario_espelhado) != 16:
                    continue
                
                # Desfaz o espelhamento
                binario = self.espelhar_binario(binario_espelhado)
                
                # Extrai apenas os 4 bits da cor (formato cccc000000000000)
                cor_bin = binario[:4]
                indice_cor = int(cor_bin, 2)
                
                # Verifica limites
                if indice_cor >= len(self.lista_cores):
                    continue
                
                # Calcula a posição x,y a partir do índice linear
                x = i % 128
                y = i // 128
                
                # Define a cor do pixel
                cor = self.lista_cores[indice_cor]
                if not isinstance(cor, QtGui.QColor):
                    cor = QtGui.QColor(cor)
                
                imagem.setPixelColor(x, y, cor)
            
            return imagem
            
        except Exception as e:
            print(f"Erro ao decodificar SCBIN: {str(e)}")
            return None
    
    def _cor_igual(self, cor1, cor2):
        """Verifica se duas cores são iguais com tolerância"""
        if not isinstance(cor1, QtGui.QColor):
            cor1 = QtGui.QColor(cor1)
        if not isinstance(cor2, QtGui.QColor):
            cor2 = QtGui.QColor(cor2)
            
        # Compara os componentes RGB
        r1, g1, b1 = cor1.getRgb()[:3]
        r2, g2, b2 = cor2.getRgb()[:3]
        
        # Usa uma pequena tolerância para comparação
        tolerancia = 5
        return (abs(r1 - r2) <= tolerancia and 
                abs(g1 - g2) <= tolerancia and 
                abs(b1 - b2) <= tolerancia) 