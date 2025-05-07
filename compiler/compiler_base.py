import os

class CompilerBase(object):
    def __init__(self):
        self.name = "CompilerBase"
        # opcode table for real instructions (6 bits)
        self.real_instructions = {
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
        
        # Virtual instructions that translate to multiple real instructions
        self.virtual_instructions = {
            "void": [
                ("nop"),
                ("nop")
            ]
        }
        
        # Data sections
        self.data_section = {}
        self.vdata_section = {}
        self.pointers = {}
        self.current_section = None
        self.data_address = 0
        self.max_memory = 65536  # Maximum memory address + 1
        
    def reg_converter(self, reg="reg(0-7)"):
        # Remove any whitespace
        reg = reg.strip()
        
        # Dictionary to convert reg to binary
        reg_decodifier = {
            "reg0": "000",
            "reg1": "100",
            "reg2": "010",
            "reg3": "110",
            "reg4": "001",
            "reg5": "101",
            "reg6": "011",
            "reg7": "111"
        }
        
        if reg not in reg_decodifier:
            raise ValueError(f"Registrador inválido: {reg}")
            
        return reg_decodifier[reg]

    def process_data_section(self, lines, start_index):
        """Process .data section and return the last processed line index"""
        current_line = start_index
        data_values = []
        length = 0
        
        while current_line < len(lines):
            line = lines[current_line].strip()
            
            # Remove comments
            if "#" in line:
                line = line[:line.index("#")].strip()
                
            if not line:
                current_line += 1
                continue
                
            if line == "end":
                break
            elif line.startswith("init"):
                try:
                    length = int(line.split()[1])
                except (IndexError, ValueError):
                    raise ValueError(f"Invalid init value in data section")
            elif line.startswith("0x"):
                try:
                    value = int(line[2:], 16)
                    data_values.append(format(value, '016b'))
                except ValueError:
                    raise ValueError(f"Invalid hex value in data section: {line}")
                    
            current_line += 1
            
        if len(data_values) > length:
            raise ValueError(f"Data section overflow: declared {length}, got {len(data_values)}")
            
        # Pad with zeros if needed
        while len(data_values) < length:
            data_values.append("0000000000000000")
            
        self.data_section[self.data_address] = data_values
        start_addr = self.data_address
        self.data_address += length
        return current_line, start_addr

    def calculate_vdata_address(self, vdata_size):
        """Calculate VRAM start address based on its size"""
        return self.max_memory - vdata_size

    def process_vdata_section(self, lines, start_index):
        """Process .Vdata section and return the last processed line index"""
        current_line = start_index
        vdata_values = []
        length = 0
        
        while current_line < len(lines):
            line = lines[current_line].strip()
            
            # Remove comments
            if "#" in line:
                line = line[:line.index("#")].strip()
                
            if not line:
                current_line += 1
                continue
                
            if line == "end":
                break
            elif line.startswith("init"):
                try:
                    length = int(line.split()[1])
                except (IndexError, ValueError):
                    raise ValueError(f"Invalid init value in Vdata section")
            elif line.startswith("0x"):
                try:
                    value = int(line[2:], 16)
                    vdata_values.append(format(value, '016b'))
                except ValueError:
                    raise ValueError(f"Invalid hex value in Vdata section: {line}")
                    
            current_line += 1
            
        if len(vdata_values) > length:
            raise ValueError(f"VData section overflow: declared {length}, got {len(vdata_values)}")
            
        # Pad with zeros if needed
        while len(vdata_values) < length:
            vdata_values.append("0000000000000000")
            
        # Calculate VRAM start address to end at max_memory - 1 (0xFFFF)
        self.vdata_address = self.max_memory - length
        
        # Store the values
        self.vdata_section[self.vdata_address] = vdata_values
        
        return current_line, self.vdata_address
        
    def process_pointer(self, line):
        """Process pointer declaration"""
        parts = line.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid pointer declaration: {line}")
            
        pointer_name = parts[0].split()[1].strip()
        address = parts[1].strip()
        
        # Convert hex address to binary
        if address.startswith("0x"):
            try:
                addr_value = int(address[2:], 16)
            except ValueError:
                raise ValueError(f"Invalid hex address in pointer: {address}")
        else:
            try:
                addr_value = int(address)
            except ValueError:
                raise ValueError(f"Invalid address in pointer: {address}")
            
        self.pointers[pointer_name] = format(addr_value, '016b')
        
    def resolve_pointer(self, instruction):
        """Resolve pointer references in instructions"""
        parts = instruction.split()
        result = []
        
        for part in parts:
            if part in self.pointers:
                result.append(self.pointers[part])
            else:
                result.append(part)
                
        return " ".join(result)

    def convert_line(self, assembly_text = str()):
        # Remove comments starting with #
        if "#" in assembly_text:
            assembly_text = assembly_text[:assembly_text.index("#")].strip()
            
        if not assembly_text or assembly_text.isspace():
            return None
            
        # Handle special directives
        if assembly_text in [".data", ".Vdata", "end"]:
            return None
            
        # Check if it's an IDATE instruction
        if assembly_text.lower().startswith("idate"):
            parts = assembly_text.split()
            if len(parts) > 1:
                value = parts[1]
                if value.startswith("0x"):
                    return format(int(value[2:], 16), '016b')
            return "0000000000000000"

        # Process pointer declaration
        if assembly_text.startswith("pointer"):
            self.process_pointer(assembly_text)
            return None
            
        # Skip init directive in data sections
        if assembly_text.startswith("init"):
            return None
            
        # Handle hex values in data sections
        if assembly_text.startswith("0x"):
            try:
                value = int(assembly_text[2:], 16)
                return format(value, '016b')
            except ValueError:
                raise ValueError(f"Invalid hex value: {assembly_text}")
            
        # Resolve any pointer references
        assembly_text = self.resolve_pointer(assembly_text)
        
        # Process instructions
        parts = assembly_text.split(",")
        instruction_parts = parts[0].strip().split()
        if not instruction_parts:
            return None
            
        instruction = instruction_parts[0]
        
        # Check for virtual instructions
        if instruction in self.virtual_instructions:
            virtual_seq = self.virtual_instructions[instruction]
            result = []
            for real_inst, args in virtual_seq:
                # Map virtual instruction arguments to real instruction arguments
                mapped_args = []
                for arg in args:
                    if arg in instruction_parts[1:]:
                        mapped_args.append(instruction_parts[instruction_parts.index(arg)])
                    else:
                        mapped_args.append(arg)
                        
                real_assembly = real_inst + " " + ",".join(mapped_args)
                binary = self._convert_real_instruction(real_assembly)
                if binary:
                    result.append(binary)
                    
            return result if len(result) > 1 else result[0] if result else None
            
        # Process real instruction
        return self._convert_real_instruction(assembly_text)

    def _convert_real_instruction(self, assembly_text):
        """Process a real instruction"""
        parts = [p.strip() for p in assembly_text.split(",")]
        instruction_parts = parts[0].strip().split()
        instruction = instruction_parts[0]
        
        if instruction in self.real_instructions:
            opcode = self.real_instructions[instruction]
            regs = ["000", "000", "000"]
            flag = "0"
            
            try:
                if instruction == "nop":
                    pass
                else:
                    all_regs = []
                    # Get register from instruction if present
                    if len(instruction_parts) > 1:
                        all_regs.append(instruction_parts[1])
                    # Get remaining registers from comma-separated list
                    if len(parts) > 1:
                        all_regs.extend(parts[1:])
                    
                    # Convert registers
                    for i, reg in enumerate(all_regs):
                        if i < 3:  # Maximum 3 registers
                            regs[i] = self.reg_converter(reg)
                    
                    # Set flag for conditional jumps
                    if instruction == "jumpC":
                        flag = "1"
                
                binary_text = opcode + regs[0] + regs[1] + regs[2] + flag
                return binary_text
                
            except Exception as e:
                raise ValueError(f"Erro ao processar instrução '{instruction}': {str(e)}")
        else:
            raise ValueError(f"Instrução desconhecida: {instruction}")

    def convertdoc(self, docaddress):
        try:
            if not os.path.exists(docaddress):
                raise FileNotFoundError(f"Arquivo não encontrado: {docaddress}")

            compilation_errors = []
            instruction_output = []
            data_section = []
            vdata_section = []

            # Reset data sections
            self.data_section = {}
            self.vdata_section = {}
            self.pointers = {}
            self.data_address = 0
            self.pending_idate = None

            # Process the file
            with open(docaddress, 'r', encoding='utf-8') as doc:
                lines = [line.strip() for line in doc.readlines()]

            # First pass - process instructions
            line_num = 0
            current_address = 0
            while line_num < len(lines):
                line = lines[line_num].strip()
                
                try:
                    if not line or line.startswith("#"):
                        line_num += 1
                        continue

                    if line in [".data", ".Vdata"]:
                        # Skip data sections in first pass
                        while line_num < len(lines) and lines[line_num].strip() != "end":
                            line_num += 1
                        line_num += 1
                        continue

                    # Process instructions
                    binary_data = self.convert_line(line)
                    if binary_data:
                        if isinstance(binary_data, list):
                            for instr in binary_data:
                                instruction_output.append(instr)
                                instruction_output.append("0000000000000000")  # Default IDATE
                                current_address += 2
                        else:
                            instruction_output.append(binary_data)
                            if not line.lower().startswith("idate"):
                                instruction_output.append("0000000000000000")  # Default IDATE
                                current_address += 2
                            
                except Exception as e:
                    compilation_errors.append(f"Erro na linha {line_num + 1}: {str(e)}")
                
                line_num += 1

            # Second pass - process data sections
            self.data_address = current_address + (current_address % 2)  # Ensure even alignment
            line_num = 0
            while line_num < len(lines):
                line = lines[line_num].strip()
                
                try:
                    if line == ".data":
                        line_num, addr = self.process_data_section(lines, line_num + 1)
                        continue
                    elif line == ".Vdata":
                        line_num, addr = self.process_vdata_section(lines, line_num + 1)
                        continue
                except Exception as e:
                    compilation_errors.append(f"Erro na linha {line_num + 1}: {str(e)}")
                
                line_num += 1

            # Add data section marker and contents
            if self.data_section:
                data_section.append(f".data 0x{self.data_address:04X}")
                for values in self.data_section.values():
                    data_section.extend(values)

            # Add VRAM section if exists
            if self.vdata_section:
                for addr, values in self.vdata_section.items():
                    vdata_section.append(f".Vdata 0x{addr:04X}")
                    vdata_section.extend(values)

            if compilation_errors:
                print("\nErros de compilação encontrados:")
                for error in compilation_errors:
                    print(error)
                return False

            # Combine all sections
            final_output = instruction_output + data_section + vdata_section

            # Write output file
            output_path = os.path.join(os.path.dirname(docaddress), "output.skbin")
            with open(output_path, "w", encoding='utf-8') as output_file:
                for binary in final_output:
                    if binary.startswith("."):
                        output_file.write(binary + "\n")
                    else:
                        output_file.write(binary.zfill(16) + "\n")
                    
            print(f"\nCompilação concluída com sucesso!")
            print(f"Arquivo de saída: {output_path}")
            print(f"Total de linhas: {len(final_output)}")
            print("\nConteúdo do arquivo binário:")
            addr = 0
            for binary in final_output:
                if binary.startswith("."):
                    print(f"\n{binary}")
                else:
                    print(f"{addr:04X}: {binary}")
                    addr += 1
            return True

        except Exception as e:
            print(f"Erro inesperado durante a compilação: {str(e)}")
            return False

if __name__ == "__main__":
    import os
    compiler = CompilerBase()
    arquivo = input("qual arquivo deseja compilar? ")
    if arquivo == "":
        print("Nenhum arquivo fornecido. Usando arquivo padrão 'test.asm'.")
        arquivo = "test.asm"
    test_file = os.path.join(os.path.dirname(__file__), "..", arquivo)
    print(f"Compilando arquivo: {test_file}")
    if compiler.convertdoc(test_file):
        print("Compilação completa. Verifique output.skbin para resultados.")