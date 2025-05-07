#!/usr/bin/env python3
import sys
import os
from compiler_base import CompilerBase

def main():
    compiler = CompilerBase()
    
    if len(sys.argv) < 2:
        print("Uso: compiler_terminal.py <arquivo_entrada> [arquivo_saida]")
        print("  arquivo_entrada: arquivo .sklanguage para compilar")
        print("  arquivo_saida: (opcional) arquivo .skbin de saída")
        return
    
    input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = os.path.splitext(input_file)[0] + '.skbin'
    
    print(f"Compilando {input_file}...")
    if compiler.convertdoc(input_file):
        # Move/rename the output file if needed
        default_output = os.path.join(os.path.dirname(input_file), "output.skbin")
        if os.path.exists(default_output) and default_output != output_file:
            try:
                with open(default_output, 'r') as src, open(output_file, 'w') as dst:
                    dst.write(src.read())
                os.remove(default_output)
                print(f"Arquivo compilado com sucesso: {output_file}")
            except Exception as e:
                print(f"Erro ao salvar arquivo de saída: {e}")
        else:
            print(f"Arquivo compilado com sucesso: {default_output}")
    else:
        print("Erro durante a compilação")

if __name__ == "__main__":
    main()