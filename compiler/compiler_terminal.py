#!/usr/bin/env python3
import sys
import os
# Adjusted import to be more specific, assuming project root is in PYTHONPATH
from compiler.compiler_base_A import CompilerBase

def main():
    compiler = CompilerBase()
    
    if len(sys.argv) < 2 or len(sys.argv) > 3: # Expect 2 or 3 arguments
        print("Uso: compiler_terminal.py <arquivo_entrada> [arquivo_saida]", file=sys.stderr)
        print("  arquivo_entrada: arquivo .sklanguage para compilar", file=sys.stderr)
        print("  arquivo_saida: (opcional) arquivo .skbin de saída", file=sys.stderr)
        sys.exit(1) # Exit with error code
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Erro: Arquivo de entrada não encontrado: {input_file}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Default output is input_filename.skbin in the same directory as input_file
        output_file = os.path.splitext(input_file)[0] + '.skbin'
    
    # Ensure the output directory exists if a full path is given
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Erro ao criar diretório de saída '{output_dir}': {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Compilando {input_file} para {output_file}...") # To stdout for progress
    
    # convertdoc outputs 'output.skbin' in the *input file's directory*
    # We need to manage this output relative to the desired output_file path.
    input_file_dir = os.path.dirname(os.path.abspath(input_file))
    hardcoded_convertdoc_output = os.path.join(input_file_dir, "output.skbin")

    # Clean up pre-existing hardcoded output file if it's not the target output, to avoid confusion
    if os.path.exists(hardcoded_convertdoc_output) and hardcoded_convertdoc_output != os.path.abspath(output_file):
        try:
            os.remove(hardcoded_convertdoc_output)
        except OSError as e:
            print(f"Aviso: Não foi possível remover o arquivo de saída antigo '{hardcoded_convertdoc_output}': {e}", file=sys.stderr)

    if compiler.convertdoc(input_file): # This prints its own errors to stdout from CompilerBaseA
        # convertdoc succeeded, now ensure file is at output_file
        if hardcoded_convertdoc_output != os.path.abspath(output_file):
            try:
                # Ensure the source (hardcoded_convertdoc_output) actually exists after successful convertdoc
                if not os.path.exists(hardcoded_convertdoc_output):
                     print(f"Erro: Arquivo de saída esperado '{hardcoded_convertdoc_output}' não foi criado pelo compilador.", file=sys.stderr)
                     sys.exit(1)
                shutil.move(hardcoded_convertdoc_output, output_file)
                print(f"Arquivo compilado com sucesso: {output_file}") # To stdout
            except Exception as e:
                print(f"Erro ao mover/renomear arquivo de saída para '{output_file}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # If hardcoded_convertdoc_output is the same as output_file, it's already there.
            print(f"Arquivo compilado com sucesso: {output_file}") # To stdout
    else:
        # convertdoc returned False, meaning compilation errors occurred.
        # CompilerBaseA.convertdoc already prints detailed errors to stdout.
        # We'll print a general error to stderr and exit.
        print("Erro durante a compilação. Verifique as mensagens acima.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import shutil # Added import here
    main()