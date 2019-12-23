# Script python to make assembler from .asm to .hack
import re
import sys


class Assembler:
    def __init__(self, file_in='add/Add.asm'):
        self.symbol_list = {
            'SP' : 0,
            'LCL' : 1,
            'ARG' : 2,
            'THIS' : 3,
            'THAT' : 4,
            '''
            'R0' : 0,
            'R1' : 1,
            'R2' : 2,
            'R3' : 3,
            'R4' : 4,
            'R5' : 5,
            'R6' : 6,
            'R7' : 7,
            'R8' : 8,
            'R9' : 9,
            'R10' : 10,
            'R11' : '11',
            'R12' : '12',
            'R13' : '13',
            'R14' : '14',
            'R15' : '15',
            '''
            'SCREEN' : 16384,
            'KBD' : 24576,
        }
        self.name_assembly = file_in
        self.assembly_file = open(file_in, 'r')
        self.mnemonics = {0: {   # = 0
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'A+D': '000010',  # Repeated from the line above D+A == A+D
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101'
        }, 1: {  # a = 1
            # '': '101010',
            # '': '111111',
            # '': '111010',
            # '': '001100',
            'M': '110000',
            # '': '001101',
            '!M': '110001',
            # '': '001111',
            '-M': '110011',
            # '': '011111',
            'M+1': '110111',
            # '': '001110',
            'M-1': '110010',
            'D+M': '000010',
            'M+D': '000010',  # Repeated from the line above D+M == M+D
            'D-M': '010011',
            'M-D': '000111',
            'D&M': '000000',
            'D|M': '010101'
            }, 'd': {  # destination
            '': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111'
            }, 'j': {  # jumpers
            '': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
            }
        }

    def identify_symbols(self):
        code_clean = []
        lines_count = 0

        for line in self.assembly_file:
            if len(line) > 1:  # Is not empty line
                line = line.split('//')[0].replace('\n', '').replace(' ', '')

                if line != '':  # Get Symbols
                    symbol = re.search(r'\((.+?)\)', line)
                    if symbol:
                        self.symbol_list[symbol.group(1)] = lines_count
                    else:
                        code_clean.append(line)
                        lines_count += 1

        self.assembly_file = code_clean
        return self.assembly_file

    def change_variable(self):
        code_clean = []
        for line in self.assembly_file:
            if ('@' in line) and ('@R' not in line):  # New variable
                try:  # If there is a idicative number of position in memory
                    _ = int(line.split("@")[1])  # XXX: Fix the part!
                    code_clean.append(line)
                except Exception:
                    # XXX: Make @screen symbol reference
                    if line.split('@')[1] in self.symbol_list:
                        code_clean.append(
                            '@' + str(self.symbol_list[line.split('@')[1]]))
                    else:
                        self.symbol_list[line.split('@')[1]] = \
                            self.get_pos_free_memory()
                        code_clean.append(
                            '@' + str(self.symbol_list[line.split('@')[1]]))
            elif '@R' in line:  # New variable register
                try:  # If there is a idicative number of position in memory
                    _ = int(line.split("@R")[1])  # XXX: Fix the part!
                    code_clean.append('@'+str(line.split("@R")[1]))
                except Exception:
                    # XXX: Make @screen symbol reference
                    if line.split('@R')[1] in self.symbol_list:
                        code_clean.append(
                            '@' + str(self.symbol_list[line.split('@')[1]]))
                    else:
                        self.symbol_list[line.split('@')[1]] = \
                            self.get_pos_free_memory()
                        code_clean.append(
                            '@' + str(self.symbol_list[line.split('@')[1]]))

            else:  # If the line there is not a variable
                code_clean.append(line)

        self.assembly_file = code_clean
        return self.assembly_file

    def get_pos_free_memory(self):
        for new_position in range(16, 16000):
            if new_position not in self.symbol_list.values():
                return new_position

    def change_symbols(self):
        assembly_source = self.assembly_file

        for line in enumerate(assembly_source):
            for symbol, number_line in self.symbol_list.items():
                # if line[1].find(symbol) > 0:
                if line[1] in symbol:
                    self.assembly_file[line[0]] = line[1].\
                        replace(str(symbol), str(number_line))
                    break

    def dec2bin(self, num_dec=0):
        """
        dec2bin return a binary 16-bits string from decimal number
        """
        return str(bin(int(num_dec))).replace('0b', '').zfill(16)

    def get_key_by_value(self, pos=0):
        key_list = list(self.symbol_list.keys())
        val_list = list(self.symbol_list.values())

        return key_list[val_list.index(pos)]

    def code_scan(self):
        for line in enumerate(self.assembly_file):
            a_instruction = '@'

            if a_instruction in line[1]:

                if '@R' in line[1]:
                    a_instruction = '@R'

                    if isinstance(line[1].split(a_instruction)[1], int):
                        self.assembly_file[line[0]] = self.dec2bin(
                                    line[1].split(a_instruction)[1])
                    else:
                        self.assembly_file[line[0]] =\
                                self.get_pos_free_memory()
                else:
                    symbol_aux = line[1].split(a_instruction)[1]
                    try:
                        _ = int(symbol_aux)  # XXX: Enchance the part!!!
                        if symbol_aux in self.symbol_list:
                            self.assembly_file[line[0]] = self.dec2bin(
                                            self.symbol_list[symbol_aux])
                        else:
                            if int(symbol_aux) in self.symbol_list.values():
                                key_symbol = self.get_key_by_value(
                                                            int(symbol_aux))
                                self.assembly_file[line[0]] = self.dec2bin(
                                            self.symbol_list[key_symbol])
                            else:
                                self.symbol_list[symbol_aux] = int(symbol_aux)
                                self.assembly_file[line[0]] = self.dec2bin(
                                            self.symbol_list[symbol_aux])
                    except Exception:
                        if symbol_aux in self.symbol_list:
                            self.assembly_file[line[0]] = self.dec2bin(
                                            self.symbol_list[symbol_aux])
                        else:  # Register symbol and change a variable
                            self.symbol_list[symbol_aux] = \
                                self.get_pos_free_memory()
                            self.assembly_file[line[0]] = self.dec2bin(
                                            self.symbol_list[symbol_aux])

            else:  # C-Instructions
                # part a - Comparison
                if ';' in line[1]:  # There is JMP in line
                    if '=' in line[1]:
                        a = 1 if 'M' in line[1].split(';')[0].\
                                                        split('=')[1] else 0
                    else:
                        a = 1 if 'M' in line[1].split(';')[0] else 0
                else:
                    if '=' in line[1]:
                        a = 1 if 'M' in line[1].split('=')[1] else 0
                    else:
                        a = 1 if 'M' in line[1] else 0

                # part c - Commands
                if '=' in line[1]:
                    c_instruction_aux = line[1].split('=')[1]
                else:
                    c_instruction_aux = line[1]

                if ';' in line[1]:
                    c_instruction_aux = c_instruction_aux.split(';')[0]

                c_result = self.mnemonics[a][c_instruction_aux]

                # part d - Destination
                if '=' in line[1]:
                    d_instruction_aux = line[1].split('=')[0]
                    d_result = self.mnemonics['d'][d_instruction_aux]
                else:
                    d_result = self.mnemonics['d']['']

                # part j - Jumps
                if ';' in line[1]:
                    j_instruction_aux = line[1].split(';')[1]
                    j_result = self.mnemonics['j'][j_instruction_aux]
                else:
                    j_result = self.mnemonics['j']['']

                self.assembly_file[line[0]] = '111' + \
                    str(a) + str(c_result) +\
                    str(d_result) + str(j_result)

        return self.assembly_file

    def source(self):
        for line in enumerate(self.assembly_file):
            print(line[0], ' ', line[1])

    def save(self):
        f = open(sys.argv[1].replace('asm', 'hack'), 'w')
        for line in self.assembly_file:
            f.write(str(line) + '\n')
        f.close()

    def symbols(self):
        for key, value in self.symbol_list.items():
            print(key, '\t-\t', value)


if __name__ == '__main__':
    file_hasm = sys.argv[1]
    a = Assembler(file_hasm)
    a.identify_symbols()
    a.change_variable()
    a.code_scan()
    a.save()
    # a.source()
    a.symbols()
