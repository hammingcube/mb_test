from transpile import evaluate
import unittest


def tests():
    fields = {
        1: 'id',
        2: 'name',
        3: 'date_joined',
        4: 'age',
    }
    macros = {
        'is_joe': ["=", ["field", 2], "joe"],
    }
    expressions = [
        ["=", ["field", 3], None],
        [">", ["field", 4], 35],
        ["AND", ["<", ["field", 1],  5], ["=", ["field", 2], "joe"]],
        ["OR", ["!=", ["field", 3], "2015-11-01"], ["=", ["field", 1], 456]],
        ["AND", 
         ["!=", ["field", 3], None],
         ["!=", ["field", 2], None], 
         ["OR", [">", ["field", 4], 25], ["=", ["field", 2], "Jerry"]]],
         ["is_empty", ["field", 3]],
        ["AND", ["<", ["field", 1],  5], ["macro", "is_joe"]],
    ]
    for expr in expressions:
        e = evaluate(fields, expr, macros)
        print(e)



class TestTranspile(unittest.TestCase):
    def test_main(self):
    	tests()

       

if __name__ == '__main__':
    unittest.main()