import pars
import scanner

input_string = '''
 PRINT x;
    IF quantity THEN
        total := total;
        tax := 0.05;
    ENDIF;
'''

print(input_string)

scanner = scanner.Scanner(input_string)
# print scanner.tokens

parser = pars.Parser(scanner)
parser.start()
