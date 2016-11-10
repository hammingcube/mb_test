def type_of(expr):
    if type(expr) == list and len(expr) > 0 and expr[0] == 'field':
        return 'FIELD_LOOKUP'
    if type(expr) in (int, float, str, type(None)):
        return 'LITERAL'
    if type(expr) == list and len(expr) > 0:
        return 'BINARY_OPERATION'


def eval_field(fields, expr):
    return fields[expr[1]]

def eval_literal(fields, expr):
    if type(expr) in (int, float):
        return str(expr)
    if type(expr) == str:
        return "'{}'".format(expr)
    if expr is None:
        return 'NULL'

def evaluate(fields, expr, depth=0):
    type_of_expr = type_of(expr)
    if type_of_expr == 'LITERAL':
        return eval_literal(fields, expr)
    elif type_of_expr == 'FIELD_LOOKUP':
        return eval_field(fields, expr)
    elif type_of_expr == 'BINARY_OPERATION':
        op, lhs, rhs = expr[0], expr[1], expr[2]
        lhs_str = evaluate(fields, lhs, depth+1)
        rhs_str = evaluate(fields, rhs, depth+1)
        if op in ('=', '!=') and (lhs_str == 'NULL' or rhs_str == 'NULL'):
            op_str = {'=': 'IS', '!=': 'IS NOT'}[op]
        elif op == '!=':
            op_str = '<>'
        else:
            op_str = op
        return '{} {} {}'.format(lhs_str, op_str, rhs_str)

def tests():
    fields = {
        1: 'id',
        2: 'name',
        3: 'date_joined',
        4: 'age',
    }
    expressions = [
        ["=", ["field", 3], None],
        [">", ["field", 4], 35],
        ["AND", ["<", ["field", 1],  5], ["=", ["field", 2], "joe"]],
        ["OR", ["!=", ["field", 3], "2015-11-01"], ["=", ["field", 1], 456]],
        ["AND", 
         ["!=", ["field", 3], None], 
         ["OR", [">", ["field", 4], 25], ["=", ["field", 2], "Jerry"]]]
    ]
    for expr in expressions:
        e = evaluate(fields, expr)
        print(e)

tests()