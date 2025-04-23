def reg_converter(self,reg="reg(0-3)", type="numerical"or"positional"):
    if reg != 'reg0' and reg != 'reg1' and reg != 'reg2' and reg != 'reg3':
        raise TypeError(f"reg inesistente fornecido")
    
    if type != 'numerical' and type != "positional" :
        raise TypeError("typo de codificação de registrador não foi respeitado")
    
    reg_numerical = {
        "reg0":"00",
        "reg1":"01",
        "reg2":"10",
        "reg3":"11"
    }    
    reg_positional = {
        "reg0,reg1":"1100",
        "reg1,reg2":"0110",
        "reg2,reg3":"0011",
        "reg0,reg3":"1001",
        "reg1,reg3":"0101",
        "reg0,reg2":"1010"
    }
    
    if reg not in reg_numerical and type == "numerical" :
        raise  TypeError(f'o argumento reg fornecido não é compativel com o tipo fornecido: {reg} não é {type}')

    
    if reg not in reg_positional and type == "positional" :
        raise  TypeError(f'o argumento reg fornecido não é compativel com o tipo fornecido: {reg} não é {type}')


    if type == "numerical" :
        reg_bin = reg_numerical[reg]
        return reg_bin
    
    if type == "positional" :
        reg_bin = reg_positional[reg]
        return reg_bin










def convert_line(self,assembly_text = str()):
    multlinecont   = int()  # indica numero de linhas de saida do codigo binario
    multline       = bool() #indica se tem multilhinha na função
    binary_line    = []     # arrey com o codigo de saida binario


    # metodo de comverção

    assembly_line = f'1+{assembly_text}' 

    if assembly_line == '1+a':
        multline = True
        multlinecont = 2
        binary_line.append("00000000")
        binary_line.append("00000000")


    if assembly_line == '1+b':
        multline = True
        multlinecont = 3
        binary_line.append('11111111')
        binary_line.append('11111111')
        binary_line.append('11111111')


        # saida do codigo

    return binary_line, multline, multlinecont 