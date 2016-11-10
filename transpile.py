def type_of(expr):
    if type(expr) in (int, float, str, type(None)):
        return 'LITERAL'
    if type(expr) == list and len(expr) > 0:
        if expr[0] == 'field':
            return 'FIELD_LOOKUP'
        elif expr[0] == 'macro':
            return 'MACRO_LOOKUP'
    if type(expr) == list and len(expr) == 2:
        return 'UNARY_OPERATION'
    if type(expr) == list and len(expr) == 3:
        return 'BINARY_OPERATION'
    return 'MULTIARY_OPERATION'

def eval_field(fields, expr):
    return fields[expr[1]]

def eval_literal(fields, expr):
    if type(expr) in (int, float):
        return str(expr)
    if type(expr) == str:
        return "'{}'".format(expr)
    if expr is None:
        return 'NULL'

def evaluate(fields, expr, macros=None):
    type_of_expr = type_of(expr)
    if type_of_expr == 'LITERAL':
        return eval_literal(fields, expr)
    elif type_of_expr == 'FIELD_LOOKUP':
        return eval_field(fields, expr)
    elif type_of_expr == 'MACRO_LOOKUP':
        if macros and macros.get(expr[1]):
            return evaluate(fields, macros[expr[1]], macros)
        return ''
    elif type_of_expr == 'UNARY_OPERATION':
        computed = evaluate(fields, expr[1], macros)
        d = {
            'is_empty': 'IS NULL',
            'is_non_empty': 'IS NOT NULL',
        }
        return '({} {})'.format(computed, d[expr[0]])
    elif type_of_expr == 'BINARY_OPERATION':
        op, lhs, rhs = expr[0], expr[1], expr[2]
        lhs_str = evaluate(fields, lhs, macros)
        rhs_str = evaluate(fields, rhs, macros)
        if op in ('=', '!=') and (lhs_str == 'NULL' or rhs_str == 'NULL'):
            op_str = {'=': 'IS', '!=': 'IS NOT'}[op]
        elif op == '!=':
            op_str = '<>'
        else:
            op_str = op
        return '({} {} {})'.format(lhs_str, op_str, rhs_str)
    op_str = ' {} '.format(expr[0])
    return '({})'.format(op_str.join([evaluate(fields, e, macros) for e in expr[1:]]))

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

tests()