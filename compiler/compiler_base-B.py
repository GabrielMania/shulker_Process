import os

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
            "pointer":1,
            "store":2,
            "label":3
        }
    def preprocessing(self, codeIN, codeOUT):
        try:
            with open(codeIN, 'r') as infile, open(codeOUT, 'w') as outfile:
                instructcont = 0
                labellist = {}
                pointerlist = {}
                for line in infile:
                    #logic to preprocess the code
                    # remove comments and empty lines and trash
                    line = line.strip()
                    line = line.replace(';','')
                    line = line.replace('\t','')
                    print(line)
                    if "#" in line:
                        line = line.split("#")
                        line = line[0]
                    
                    lineparts = line.split(' ')
                    if lineparts[0] in self.instructions:
                        instructcont += instructcont
                    #label tratament
                    if lineparts[0] == self.compilercomands[3]:
                        this_label_address = instructcont + 1
                        label_index = lineparts[1].removesuffix(':')
                        line = line.removesuffix("):")
                        line = line.replace("label (",f"dload reg7 {this_label_address}\nnop")
                        labellist[label_index] = line
                    #pointers tratament
                    if lineparts[0] == self.compilercomands[1]:
                        address = lineparts[3]
                        chave = lineparts[1]
                        chave = chave.removeprefix("(")
                        chave = chave.removesuffix(")")
                        pointerlist[chave] = address
                    #store data tratament
                    if lineparts[0] == self.compilercomands[2] :



                    #end of logic
                    outfile.write(line)
        except FileNotFoundError:
            print(f"Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
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
    
    def compile(self, arquivoIN, arquivoOUT):
        self.preprocessing(arquivoIN,arquivoOUT)
        self.processing(arquivoIN,arquivoOUT)
        self.postprocessing(arquivoIN,arquivoOUT)