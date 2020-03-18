import pars
import scanner

input_string = '''
{
    "$id": "https://example.com/person.schema.json" ,
    "$shema": "http://json-schema.org/draft-07/schema#"
}
'''

print(input_string)

scanner = scanner.Scanner(input_string)
# print scanner.tokens

parser = pars.Parser(scanner)
parser.start()
