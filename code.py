class Code:
    def __init__(self, in_parsed_lines, in_filepath):
        self.filepath = in_filepath
        self.parsed_lines = in_parsed_lines
        self.symbol_table = {}
        self.jump_table = {}
        self.dest_table = {}
        self.comp_table = {}
        self.n = 16
        self.init_predefined()
        self.init_jump_talbe()
        self.init_dest_table()
        self.init_comp_table()

    def init_comp_table(self):
        self.comp_table['0'] = '101010'
        self.comp_table['1'] = '111111'
        self.comp_table['-1'] = '111010'
        self.comp_table['D'] = '001100'
        self.comp_table['A'] = '110000'
        self.comp_table['M'] = '110000'
        self.comp_table['!D'] = '001101'
        self.comp_table['!A'] = '110001'
        self.comp_table['!M'] = '110001'
        self.comp_table['-D'] = '001111'
        self.comp_table['-A'] = '110011'
        self.comp_table['-M'] = '110011'
        self.comp_table['D+1'] = '011111'
        self.comp_table['A+1'] = '110111'
        self.comp_table['M+1'] = '110111'
        self.comp_table['D-1'] = '001110'
        self.comp_table['A-1'] = '110010'
        self.comp_table['M-1'] = '110010'
        self.comp_table['D+A'] = '000010'
        self.comp_table['D+M'] = '000010'
        self.comp_table['D+A'] = '000010'
        self.comp_table['D-A'] = '010011'
        self.comp_table['D-M'] = '010011'
        self.comp_table['A-D'] = '000111'
        self.comp_table['M-D'] = '000111'
        self.comp_table['D&A'] = '000000'
        self.comp_table['D&M'] = '000000'
        self.comp_table['D|A'] = '010101'
        self.comp_table['D|M'] = '010101'

    def init_dest_table(self):
        self.dest_table['null'] = '000'
        self.dest_table['M'] = '001'
        self.dest_table['D'] = '010'
        self.dest_table['MD'] = '011'
        self.dest_table['A'] = '100'
        self.dest_table['AM'] = '101'
        self.dest_table['AD'] = '110'
        self.dest_table['AMD'] = '111'

    def init_jump_talbe(self):
        self.jump_table['null'] = '000'
        self.jump_table['JGT'] = '001'
        self.jump_table['JEQ'] = '010'
        self.jump_table['JGE'] = '011'
        self.jump_table['JLT'] = '100'
        self.jump_table['JNE'] = '101'
        self.jump_table['JLE'] = '110'
        self.jump_table['JMP'] = '111'

    def init_predefined(self):
        for i in range(16):
            self.symbol_table['R' + str(i)] = i
        self.symbol_table['SCREEN'] = 16384
        self.symbol_table['KBD'] = 24576
        self.symbol_table['SP'] = 0
        self.symbol_table['LCL'] = 1
        self.symbol_table['ARG'] = 2
        self.symbol_table['THIS'] = 3
        self.symbol_table['THAT'] = 4


    def generate_bin_code(self):
        curr_code = ''
        with open(self.filepath, 'w') as bin_file:
            for line in self.parsed_lines:
                if line.type == 'L':
                    self.symbol_table[line.symb] = line.addr
            for cmd in self.parsed_lines:
                if cmd.type == 'A':
                    if self.RepresentsInt(cmd.address):
                        bin_file.write(format(int(cmd.address), '016b') + "\n")
                    elif cmd.address in self.symbol_table:
                        bin_file.write(format(self.symbol_table[cmd.address], '016b') + "\n")
                    else:
                        self.symbol_table[cmd.address] = self.n
                        bin_file.write(format(self.n, '016b') + "\n")
                        self.n += 1
                elif cmd.type == 'C':
                    opcode = '111'
                    comp = self.comp_table[cmd.comp]
                    dest = self.dest_table[cmd.dest]
                    jump = self.jump_table[cmd.jump]
                    if 'M' in cmd.comp:
                        a = '1'
                    else:
                        a = '0'
                    bin_file.write(opcode + a + comp + dest + jump + "\n")

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False