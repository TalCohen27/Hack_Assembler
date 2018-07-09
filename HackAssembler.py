import sys
import Parser
import code

if __name__ == "__main__":
    output_file = (sys.argv[1]).replace('asm', 'hack')
    parser = Parser.Parser(sys.argv[1])
    (code.Code(parser.parse(), output_file)).generate_bin_code()
