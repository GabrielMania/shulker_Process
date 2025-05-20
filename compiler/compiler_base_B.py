import sortedcontainers as st
import traceback
class CompilerBase(object):
    def __init__(self):
        self.name = "CompilerBase"
        # opcode table for instructions (6 bits)
        self.instructions = {
            #CPU
            "nop":          "000000",
            "add":          "100000",
            "bshift":       "010000",
            "not":          "110000",
            "or":           "001000",
            "xor":          "101000",
            "and":          "011000",
            "sizeC":        "111000",
            "igual":        "000100",
            "Ttrue":        "100100",
            "limp":         "010100",
            "jump":         "110100",
            "jumpC":        "110100",
            "dload":        "001100",
            "inc":          "101100",
            "pop":          "011100",
            "push":         "011100",
            "write":        "111100",
            "read":         "000010",
            #GPU
            "drawP":        "100010",
            "drawS":        "010010",
            "drawBg":       "110010",
            "RdrawBg":      "001010",
        }
        #registry table (3 bits)
        self.registers = {
            "r0": "000",
            "r1": "100",
            "r2": "010",
            "r3": "110",
            "r4": "001",
            "r5": "101",
            "r6": "011",
            "r7": "111"
        }
        self.compilercomands = {
            1:"pointer",
            2:"store",
            3:"label"
        }
        #caracteres compativeis com o ascii
        self.caracteres = {
            'NUL': '00000000',  # Nulo
            'SOH': '00000001',  # Início de cabeçalho
            'STX': '00000010',  # Início de texto
            'ETX': '00000011',  # Fim de texto
            'EOT': '00000100',  # Fim de transmissão
            'ENQ': '00000101',  # Consulta; inquirição
            'ACK': '00000110',  # Confirmação
            'BEL': '00000111',  # Campainha; sinal sonoro
            'BS': '00001000',   # Voltar
            'HT': '00001001',   # Tabulação horizontal
            'LF': '00001010',   # Nova linha
            'VT': '00001011',   # Tabulação vertical
            'FF': '00001100',   # Alimentação de formulário
            'CR': '00001101',   # Retorno do carro
            'SO': '00001110',   # Mover para fora
            'SI': '00001111',   # Mover para dentro
            'DLE': '00010000',  # Escape do linque de dados
            'DC1': '00010001',  # Controle de dispositivo 1 (XON)
            'DC2': '00010010',  # Controle de dispositivo 2
            'DC3': '00010011',  # Controle de dispositivo 3 (XOFF)
            'DC4': '00010100',  # Controle de dispositivo 4
            'NAK': '00010101',  # Confirmação negativa
            'SYN': '00010110',  # Ocioso síncrono
            'ETB': '00010111',  # Bloco de fim de transmissão
            'CAN': '00011000',  # Cancelar
            'EM': '00011001',   # Fim de mídia
            'SUB': '00011010',  # Substituir
            'ESC': '00011011',  # Escapar
            'FS': '00011100',   # Separador de arquivos
            'GS': '00011101',   # Separador de grupos
            'RS': '00011110',   # Separador de registros
            'US': '00011111',    # Separador de unidades
            ' ': '00100000',  # Espaço (código 32)
            '!': '00100001',
            '"': '00100010',
            '#': '00100011',
            '$': '00100100',
            '%': '00100101',
            '&': '00100110',
            "'": '00100111',
            '(': '00101000',
            ')': '00101001',
            '*': '00101010',
            '+': '00101011',
            ',': '00101100',
            '-': '00101101',
            '.': '00101110',
            '/': '00101111',
            '0': '00110000',
            '1': '00110001',
            '2': '00110010',
            '3': '00110011',
            '4': '00110100',
            '5': '00110101',
            '6': '00110110',
            '7': '00110111',
            '8': '00111000',
            '9': '00111001',
            ':': '00111010',
            ';': '00111011',
            '<': '00111100',
            '=': '00111101',
            '>': '00111110',
            '?': '00111111',
            '@': '01000000',
            'A': '01000001',
            'B': '01000010',
            'C': '01000011',
            'D': '01000100',
            'E': '01000101',
            'F': '01000110',
            'G': '01000111',
            'H': '01001000',
            'I': '01001001',
            'J': '01001010',
            'K': '01001011',
            'L': '01001100',
            'M': '01001101',
            'N': '01001110',
            'O': '01001111',
            'P': '01010000',
            'Q': '01010001',
            'R': '01010010',
            'S': '01010011',
            'T': '01010100',
            'U': '01010101',
            'V': '01010110',
            'W': '01010111',
            'X': '01011000',
            'Y': '01011001',
            'Z': '01011010',
            '[': '01011011',
            '\\': '01011100',  # Note a necessidade de escape para a barra invertida
            ']': '01011101',
            '^': '01011110',
            '_': '01011111',
            '`': '01100000',
            'a': '01100001',
            'b': '01100010',
            'c': '01100011',
            'd': '01100100',
            'e': '01100101',
            'f': '01100110',
            'g': '01100111',
            'h': '01101000',
            'i': '01101001',
            'j': '01101010',
            'k': '01101011',
            'l': '01101100',
            'm': '01101101',
            'n': '01101110',
            'o': '01101111',
            'p': '01110000',
            'q': '01110001',
            'r': '01110010',
            's': '01110011',
            't': '01110100',
            'u': '01110101',
            'v': '01110110',
            'w': '01110111',
            'x': '01111000',
            'y': '01111001',
            'z': '01111010',
            '{': '01111011',
            '|': '01111100',
            '}': '01111101',
            '~': '01111110'
            #128 caracteres ainda disponiveis
        }

        self.labellist = {}
        self.pointerlist = {}
        self.datadict = st.SortedDict()
        self.outitens = []
    def preprocessing(self, codeIN, codeOUT):
        try:
            with open(codeIN, 'r') as infile, open(codeOUT, 'w') as outfile:
                instructcont = 0
                for linecont in infile:
                    #logic to preprocess the code
                    # remove comments and empty lines and trash
                    line = linecont.strip()
                    line = line.replace(';','')
                    line = line.replace('\t','')
                    self.outitens.append(line)
                    if "#" in line:
                        line = line.split("#")
                        line = line[0]
                        self.outitens.append(f"removendo string na linha {linecont}, line : {line}")
                    lineparts = line.split(' ')
                    if lineparts[0] in self.instructions:
                        instructcont += instructcont
                    #label tratament
                    if lineparts[0] == self.compilercomands[3]:
                        this_label_address = instructcont
                        label_index = lineparts[1].removesuffix(':')
                        line = line.removesuffix(":")
                        hex_address = f"0x{this_label_address:04X}"
                        line = f"dload reg7 {hex_address}\nnop"
                        self.labellist[label_index] = hex_address
                        self.outitens.append(f"tratando de label na linha {linecont}, line : {line}")
                    #pointers tratament
                    if lineparts[0] == self.compilercomands[1]:
                        address = lineparts[3]
                        chave = lineparts[1]
                        chave = chave.removeprefix("(")
                        chave = chave.removesuffix(")")
                        self.pointerlist[chave] = address
                        self.outitens.append(f"tratando de pointer na linha {linecont}, line : {line}")
                        line = ""
                    #store data tratament
                    if lineparts[0] == self.compilercomands[2] :
                        self.outitens.append(f"tratando de store na linha {linecont}, line : {line}")
                        if lineparts[2] == 'in':
                            #exemplo:
                            #store {"ola"} in x
                            line = line.replace(lineparts[3],self.pointerlist[lineparts[3]])
                            line = line.replace('in ','')
                            lineparts = line.split(' ')
                            #store {"ola"} 0xffff
                            self.outitens.append(f"removendo indicador de ponteiro do store na linha {linecont}, line : {line}")
                        if "'" in lineparts[1]:
                            #exemplo:
                            #store {'a'} 0xffff
                            a = lineparts[1].replace("'","")
                            a = a.removeprefix("(")
                            a = a.removesuffix(")")
                            line = line.replace("'","")
                            caracter = self.caracteres[a]
                            line = line.replace(a,caracter)
                            lineparts = line.split(' ')
                            #store {01100001} 0xffff
                            self.outitens.append(f"tratando de caracter na linha {linecont}, line : {line}")
                        if "\"" in lineparts[1]:
                            #exemplo:
                            #store {"ola"} 0xffff
                            a = lineparts[1].replace("\"","")
                            a = a.removeprefix("{")
                            a = a.removesuffix("}")
                            line = line.replace("\"","")
                            strbin =[]
                            for i in range(len(a)):
                                strbin.append(self.caracteres[a[i]] + ',')
                            strbin = ''.join(strbin)
                            strbin = strbin.replace(" ","")
                            line = line.replace(a,strbin)
                            lineparts = line.split(' ')
                            #store {01101111,01101100,01100001} 0xffff
                            self.outitens.append(f"tratando de string na linha {linecont}, line : {line}")
                        if ',' in lineparts[1]:
                            #adiciona em uma lista os dados com uma chave sendo o endereço 
                            #exemplo:
                            #store {01101111,01101100,01100001} 0xffcc
                            address = int(lineparts[3],16)
                            dataword = lineparts[1].removeprefix("{","")
                            dataword = dataword.removesuffix("}")
                            dataword = dataword.split(',')
                            for i in range(len(dataword)):
                                self.datadict[hex(address + i)] = dataword[i]
                            line = ""
                            #linha fica vazia em endereço se torna chave para um valor
                            self.outitens.append(f"criando dicionario de dados na linha {linecont}, line : {line}")
                    #end of logic
                    if line != "":
                        outfile.write(line + '\n')
                    if line == "":
                        outfile.write(line)
        except FileNotFoundError:
            print(f"Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
    
    def processing(self, codeIN, codeOUT):
        try:
            with open(codeIN, 'r') as infile, open(codeOUT, 'w') as outfile:
                for line in infile:
                    #logic to process the code

                    
                    #end of logic
                    outfile.write(line)
        except FileNotFoundError:
            print(f"Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
    
    def postprocessing(self, codeIN, codeOUT):
        try:
            with open(codeIN, 'r') as infile, open(codeOUT, 'w') as outfile:
                for line in infile:
                    #logic to postprocess the code
                    
                    
                    #end of logic
                    outfile.write(line)
        except FileNotFoundError:
            print(f"Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
    
    def compile(self, arquivoIN, arquivoOUT):
        self.preprocessing(arquivoIN,arquivoOUT)
        #self.processing(arquivoIN,arquivoOUT)
        #self.postprocessing(arquivoIN,arquivoOUT)