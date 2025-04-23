#decodificador de assembly para binario dos registradores (usado no compilador para cada linha de assembly)
def reg_converter(reg="reg(0-7)"):
    #validação de segurança
    if reg not in ["reg0","reg1","reg2","reg3","reg4","reg5","reg6","reg7"]:
        raise TypeError(f"reg inesistente fornecido")
    # dicionario para converter o reg em binario
    reg_decodifier = {
        "reg0":"000",
        "reg1":"100",
        "reg2":"010",
        "reg3":"110",
        "reg4":"001",
        "reg5":"101",
        "reg6":"011",
        "reg7":"111"
    }    
    #conversor de reg em binario
    
    reg_binary = reg_decodifier[reg]
    return reg_binary

def convert_line(assembly_text = str()):
    
    #dados do binario de saida da linha 
    # instructcont é nescessarios para a criação de instruções virtuais
    
    instructcont = 1 #valor padrão para instruções reais
    
    #binario_line armazena o binario de saida, é um array para suportar multiplas linhas (geradas por instruções virtuais)
    
    binary_line = []
    binary_data = [instructcont, binary_line]  # array with output data

    # opcode table for real instructions (6 bits)
    
    real_instructions = {

    }
    
    # opcode table for virtual instructions (6 bits)
    
    virtual_instructions = {
     
    }

    # quebra a linha em partes, separando o opcode dos registradores
    
    assembly_text = assembly_text.split(" ")
    
    #processa linhas em assembly sejam reais ou virtuais

    """
    implementar o processador de assembly para o opcode real e/ou virtual
    """




    return binary_data





convert_line("add reg0 reg1 reg2")