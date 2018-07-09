import sys
import os
import re


class Parser:
    def __init__(self, in_filepath):
        self.filepath = in_filepath
        self.commands = []
        self.curr_inst_addr = 0

    def parse(self):
        with open(self.filepath, 'r') as asm_file:
            line = asm_file.readline()
            while line:
                line = (line.split('/', 1)[0]).strip()
                if line:
                    if line[0] == '@':
                        self.commands.append(A_Command(line.split('@')[1].strip()))
                    elif line[0] != '/' and line[0] != '(':
                        self.parse_c_command(line)
                    elif line[0] != '/' and line[0] == '(':
                        self.commands.append(L_Command(line.strip('(').strip(')'), self.curr_inst_addr))
                        self.curr_inst_addr -= 1
                    self.curr_inst_addr += 1
                line = asm_file.readline()

        return self.commands

    def parse_c_command(self, in_line):
        c_elem = re.split('=|;', in_line)
        if len(c_elem) == 2 and '=' in in_line:
            self.commands.append(C_Command(c_elem[0].strip(), c_elem[1].strip(), 'null'))
        elif len(c_elem) == 2 and ';' in in_line:
            self.commands.append(C_Command('null', c_elem[0].strip(), c_elem[1].strip()))
        elif len(c_elem) == 3:
            self.commands.append(C_Command(c_elem[0].strip(), c_elem[1].strip(), c_elem[2].strip()))


class A_Command:
    def __init__(self, in_address):
        self.address = in_address
        self.type = 'A'


class C_Command:
    def __init__(self, in_dest, in_comp, in_jump):
        self.comp = in_comp
        self.dest = in_dest
        self.jump = in_jump
        self.type = 'C'


class L_Command:
    def __init__(self, in_symb, in_addr):
        self.symb = in_symb
        self.addr = in_addr
        self.type = 'L'
