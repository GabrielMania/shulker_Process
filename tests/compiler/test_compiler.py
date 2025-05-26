import pytest
import os
import sys
import filecmp
import subprocess 
import shutil   

# Add project root to sys.path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from compiler.compiler_base_B import CompilerBase as CompilerBaseB # Alias for clarity
from compiler.compiler_base_A import CompilerBase as CompilerBaseA # For UI-related logic

# Define project_root for constructing paths to example files consistently
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
TEST_INPUTS_DIR = os.path.join(PROJECT_ROOT, "tests/compiler/test_inputs")
COMPILER_TERMINAL_SCRIPT = os.path.join(PROJECT_ROOT, "compiler/compiler_terminal.py")

# --- Tests for CompilerBaseB (compiler_base_B.py) ---

def test_successful_compilation_base_B(tmp_path):
    """
    Tests that CompilerBaseB successfully compiles a valid .asm file (the larger test.asm)
    and produces a non-empty output file.
    """
    compiler_instance = CompilerBaseB()
    input_file_name = "test.asm"
    input_file_path = os.path.join(PROJECT_ROOT, "examples/compiler", input_file_name)
    
    assert os.path.exists(input_file_path), \
        f"Input assembly file not found: {input_file_path}. " \
        f"Please ensure 'examples/compiler/{input_file_name}' exists."
    
    output_file_path = tmp_path / f"{input_file_name}.skbin"
    
    try:
        compiler_instance.compile(str(input_file_path), str(output_file_path))
    except Exception as e:
        pytest.fail(f"CompilerBaseB raised an exception during compilation of {input_file_path}: {e}\n"
                    f"Traceback: {e.__traceback__}")
        
    assert os.path.exists(output_file_path), \
        f"Output file was not created at {output_file_path} by CompilerBaseB."
    assert os.path.getsize(output_file_path) > 0, \
        f"Output file {output_file_path} created by CompilerBaseB is empty."

def test_compile_add_nop_base_B(tmp_path):
    """
    Tests CompilerBaseB compilation of simple ADD and NOP instructions.
    Checks the preprocessed output in `outitens`.
    """
    compiler_instance = CompilerBaseB()
    input_file_path = os.path.join(TEST_INPUTS_DIR, "simple_add.asm")
    output_file_path = tmp_path / "simple_add_B.skbin"

    assert os.path.exists(input_file_path), f"Test input file not found: {input_file_path}"

    compiler_instance.compile(str(input_file_path), str(output_file_path))
    
    expected_outitens = [
        "ADD R1,R2,R3",
        "NOP"
    ]
    actual_outitens = [item for item in compiler_instance.outitens if item in expected_outitens]
    assert actual_outitens == expected_outitens, \
        f"CompilerBaseB: Expected preprocessed items {expected_outitens}, got {compiler_instance.outitens}"
    
    assert os.path.exists(output_file_path), "Output file for simple_add.asm (BaseB) was not created."
    assert os.path.getsize(output_file_path) > 0, "Output file for simple_add.asm (BaseB) is empty."


def test_compile_dload_immediate_base_B(tmp_path):
    """
    Tests CompilerBaseB compilation of DLOAD instruction with an immediate value.
    Checks the preprocessed output in `outitens`.
    """
    compiler_instance = CompilerBaseB()
    input_file_path = os.path.join(TEST_INPUTS_DIR, "load_immediate.asm")
    output_file_path = tmp_path / "load_immediate_B.skbin"

    assert os.path.exists(input_file_path), f"Test input file not found: {input_file_path}"

    compiler_instance.compile(str(input_file_path), str(output_file_path))
    
    expected_outitens = [
        "DLOAD R0,0x1234"
    ]
    actual_outitens = [item for item in compiler_instance.outitens if item in expected_outitens]
    assert actual_outitens == expected_outitens, \
        f"CompilerBaseB: Expected preprocessed items {expected_outitens}, got {compiler_instance.outitens}"

    assert os.path.exists(output_file_path), "Output file for load_immediate.asm (BaseB) was not created."
    assert os.path.getsize(output_file_path) > 0, "Output file for load_immediate.asm (BaseB) is empty."


def test_compile_invalid_instruction_base_B(tmp_path):
    """
    Tests CompilerBaseB with an invalid instruction.
    """
    compiler_instance = CompilerBaseB()
    input_file_path = os.path.join(TEST_INPUTS_DIR, "invalid_instruction.asm")
    output_file_path = tmp_path / "invalid_instruction_B.skbin"

    assert os.path.exists(input_file_path), f"Test input file not found: {input_file_path}"
    try:
        compiler_instance.compile(str(input_file_path), str(output_file_path))
    except Exception as e: # BaseB's preprocessing prints errors but doesn't seem to raise them.
        pytest.fail(f"CompilerBaseB unexpectedly failed with an exception for invalid instruction: {e}")

    assert os.path.exists(output_file_path), \
        "Output file for invalid_instruction.asm (BaseB) should still be created."


def test_source_file_not_modified_base_B(tmp_path):
    """
    Tests that CompilerBaseB does not modify the source assembly file.
    """
    compiler_instance = CompilerBaseB()
    input_file_name = "simple_add.asm"
    input_file_path = os.path.join(TEST_INPUTS_DIR, input_file_name)
    
    assert os.path.exists(input_file_path), f"Test input file not found: {input_file_path}"

    temp_source_file_path = tmp_path / input_file_name
    shutil.copyfile(input_file_path, temp_source_file_path)
    
    original_content_hash = None
    with open(temp_source_file_path, 'rb') as f:
        original_content_hash = hash(f.read()) 

    output_file_path = tmp_path / "simple_add_output_B.skbin"
    compiler_instance.compile(str(temp_source_file_path), str(output_file_path))

    new_content_hash = None
    with open(temp_source_file_path, 'rb') as f:
        new_content_hash = hash(f.read())

    assert original_content_hash == new_content_hash, \
        f"Source file {temp_source_file_path} (BaseB) was modified during compilation."

# --- Tests for CompilerBaseA (compiler_base_A.py, used by UI) ---

def test_compiler_A_convertdoc_success(tmp_path):
    """
    Tests successful compilation using CompilerBaseA.convertdoc(),
    which is used by the UI (graphCompiler.py).
    """
    compiler_instance_A = CompilerBaseA()
    
    # Prepare a source file in tmp_path, because convertdoc outputs to its input's dir
    # CompilerBaseA expects lowercase instructions and register prefixes
    source_asm_content = "add reg1,reg2,reg3\nnop"
    temp_input_file = tmp_path / "test_A_input.asm"
    with open(temp_input_file, "w") as f:
        f.write(source_asm_content)
        
    expected_output_file = tmp_path / "output.skbin" # convertdoc hardcodes this output name

    # Ensure the expected output file does not exist before test
    if os.path.exists(expected_output_file):
        os.remove(expected_output_file)

    result = compiler_instance_A.convertdoc(str(temp_input_file))

    assert result is True, "CompilerBaseA.convertdoc() should return True on success."
    assert os.path.exists(expected_output_file), \
        f"Output file {expected_output_file} was not created by CompilerBaseA.convertdoc()."
    assert os.path.getsize(expected_output_file) > 0, \
        f"Output file {expected_output_file} created by CompilerBaseA.convertdoc() is empty."

def test_compiler_A_convertdoc_invalid_asm(tmp_path, capsys):
    """
    Tests CompilerBaseA.convertdoc() with an invalid ASM file.
    It should return False and print errors.
    """
    compiler_instance_A = CompilerBaseA()

    # CompilerBaseA expects lowercase instructions
    source_asm_content = "invalid_op reg1,reg2\nnop"
    temp_input_file = tmp_path / "test_A_invalid_input.asm"
    with open(temp_input_file, "w") as f:
        f.write(source_asm_content)

    expected_output_file = tmp_path / "output.skbin"
    if os.path.exists(expected_output_file): # Clean up if it exists from a previous run
        os.remove(expected_output_file)

    result = compiler_instance_A.convertdoc(str(temp_input_file))

    assert result is False, "CompilerBaseA.convertdoc() should return False for invalid ASM."
    
    # Check for error messages printed to stdout/stderr
    # Note: compiler_base_A.convertdoc prints "Erros de compilação encontrados:"
    # and then the specific errors.
    captured = capsys.readouterr()
    assert "Erros de compilação encontrados:" in captured.out or \
           "Erros de compilação encontrados:" in captured.err, \
           "Expected compilation error messages were not printed by CompilerBaseA.convertdoc()."
    assert "Instrução desconhecida: invalid_op" in captured.out or \
           "Instrução desconhecida: invalid_op" in captured.err, \
           "Specific error for 'invalid_op' not found in CompilerBaseA.convertdoc() output."
    
    # output.skbin might still be created by convertdoc, potentially empty or with partial content.
    # This behavior is fine as long as errors are reported.
    # If it exists, it's good. If not, that's also acceptable if an error occurs early.
    # For now, no strict assertion on its existence on failure.


# --- Terminal Client Tests (compiler_terminal.py) ---

def test_terminal_successful_compilation(tmp_path):
    """
    Tests successful compilation via compiler_terminal.py.
        Uses a simple, known-good lowercase ASM file compatible with CompilerBaseA.
    """
    input_file = os.path.join(TEST_INPUTS_DIR, "simple_add_lowercase.asm") # Changed input file
    output_file = tmp_path / "terminal_out_simple_add.skbin" # Adjusted output file name
    command = [sys.executable, COMPILER_TERMINAL_SCRIPT, input_file, str(output_file)]

    # Ensure PYTHONPATH for subprocess includes project root
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = f"{PROJECT_ROOT}{os.pathsep}{current_pythonpath}"
    
    result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)

    assert result.returncode == 0, \
        f"Terminal compiler exited with code {result.returncode}. Stderr: {result.stderr}"
    assert os.path.exists(output_file), "Output file was not created by terminal compiler."
    assert os.path.getsize(output_file) > 0, "Output file created by terminal is empty."
    if result.stderr:
        print(f"Warning: Stderr not empty on successful terminal compilation: {result.stderr}")


def test_terminal_non_existent_input(tmp_path):
    """
    Tests terminal client with a non-existent input file.
    """
    input_file = os.path.join(PROJECT_ROOT, "examples/compiler/non_existent_test_file.asm")
    output_file = tmp_path / "output.skbin"
    command = [sys.executable, COMPILER_TERMINAL_SCRIPT, input_file, str(output_file)]

    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = f"{PROJECT_ROOT}{os.pathsep}{current_pythonpath}"

    result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)

    assert result.returncode != 0, "Terminal compiler should exit with a non-zero code for non-existent input file."
    # Expecting the Portuguese error message from compiler_terminal.py
    assert "erro: arquivo de entrada não encontrado:" in result.stderr.lower(), \
           f"Stderr did not contain expected error message for non-existent file. Stderr: {result.stderr}"


def test_terminal_invalid_instruction_asm(tmp_path):
    """
    Tests terminal client with an assembly file containing an invalid instruction.
    """
    input_file = os.path.join(TEST_INPUTS_DIR, "invalid_instruction.asm")
    output_file = tmp_path / "invalid_out.skbin"
    command = [sys.executable, COMPILER_TERMINAL_SCRIPT, input_file, str(output_file)]

    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = f"{PROJECT_ROOT}{os.pathsep}{current_pythonpath}"

    result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)

    # CompilerBaseA (used by terminal) prints detailed errors to its STDOUT.
    # The terminal script itself prints a generic error to STDERR.
    assert "instrução desconhecida: invalid_op" in result.stdout.lower(), \
        f"Stdout should contain specific 'Instrução desconhecida' error. Stdout: {result.stdout}"
    assert "erro durante a compilação" in result.stderr.lower(), \
        f"Stderr should contain the generic error message from terminal script. Stderr: {result.stderr}"
    
    assert result.returncode != 0, \
        f"Terminal compiler should exit non-zero for invalid ASM. Exit code: {result.returncode}"
    # The following warning is now an assertion:
    # if result.returncode == 0:
    #     print(f"Warning: Terminal compiler returned 0 for an invalid ASM file. Stderr: {result.stderr}")


def test_terminal_incorrect_arguments():
    """
    Tests terminal client with an incorrect number of arguments.
    """
    command = [sys.executable, COMPILER_TERMINAL_SCRIPT, os.path.join(PROJECT_ROOT, "examples/compiler/test.asm")]
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode != 0, "Terminal compiler should exit with a non-zero code for incorrect arguments."
    assert "usage" in result.stderr.lower() or \
           "argument" in result.stderr.lower() or \
           "erro" in result.stderr.lower(), \
           f"Stderr did not contain expected usage/error message. Stderr: {result.stderr}"

# To run these tests (assuming pytest is installed):
# 1. Navigate to the project root directory in your terminal.
# 2. Run the command: pytest
# Pytest should automatically discover and run tests in the 'tests' directory.
# Alternatively, you can specify the test file: pytest tests/compiler/test_compiler.py
