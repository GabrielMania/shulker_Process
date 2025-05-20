from compiler_base_B import CompilerBase
import traceback

def test_compiler():
    try:
        # Initialize compiler
        compiler = CompilerBase()
        
        # Define input and output paths
        input_path = "C:\\Users\\srgab\\Desktop\\shulker_Process\\compiler\\test copy.asm"
        output_path = "C:\\Users\\srgab\\Desktop\\shulker_Process\\compiler\\out.skbin"
        
        # Run compiler and catch any errors
        print("Starting compilation...")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        
        # Print compiler state before compilation
        print("\nInitial compiler state:")
        print(f"Pointer list: {compiler.pointerlist}")
        print(f"Label list: {compiler.labellist}")
        print(f"Data dictionary: {compiler.datadict}")
        
        # Run compilation
        compiler.compile(input_path, output_path)
        
        # Print compiler state after compilation
        print("\nFinal compiler state:")
        print(f"Pointer list: {compiler.pointerlist}")
        print(f"Label list: {compiler.labellist}")
        print(f"Data dictionary: {compiler.datadict}")

        #print state out text
        print(f"\nCompiler state after compilation:{compiler.outitens}")

        print("\nCompilation completed successfully!")
        
    except Exception as e:
        print("\nError during compilation:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_compiler()