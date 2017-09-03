# encoding=utf-8
import sys

sys.path.append(
    "..",
)

import re
from grammer_checkers.ply import lex as lex
from grammer_checkers.ply import yacc as yacc
from util import XlsSyntaxError

# lexer ------------------------------------
# types and symbols

t_VERTICALBAR = "\|"
t_EQUAL = r"="
t_TRUE = "true"
t_PYTRUE = "True"
t_FALSE = "false"
t_PYFALSE = "False"
# ------------------

reserved = {}

tokens = list(reserved.values()) + [
    "VERTICALBAR", "EQUAL",
    'STRING', 'NUM', 'INTEGER', 'FLOAT',
    "TRUE", "FALSE", "PYTRUE", "PYFALSE",
]

def t_NUM(token):
    r'[0-9]*\.?[0-9]+((E|e)(\+|-)?[0-9]+)?'
    try:
        token.value = int(token.value)
        token.type = 'INTEGER'
        return token
    except ValueError:
        pass

    try:
        token.value = float(token.value)
        token.type = 'FLOAT'
        return token
    except ValueError:
        print("transfer error: %s", token.value)
        return token

    return token


def t_STRING(t):
    r'"(.+?)"'
    t.value = t.value[1:-1]
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])

lex_checker = lex.lex(reflags=re.UNICODE)

# parser -----------------
def p_value(p):
    '''  value : basetypex
               | extendtype'''
    p[0] = p[1]

def p_basetypex(p):
    ''' basetypex : basetype '''
    p[0] = p[1]

def p_basetype(p):
    ''' basetype : bool_val
                 | float_val
                 | int_val
                 | str_val '''
    p[0] = p[1]

def p_bool_val(p):
    ''' bool_val : TRUE
                | FALSE
                | PYTRUE
                | PYFALSE '''
    p[0] = {"true": True, "false": False, "True": True, "False": False}[p[1]]

def p_float_val(p):
    ''' float_val : FLOAT '''
    p[0] = float(p[1])

def p_int_val(p):
    ''' int_val : INTEGER '''
    p[0] = int(p[1])

def p_str_val(p):
    ''' str_val : STRING '''
    p[0] = str(p[1])

def p_extendtype(p):
    ''' extendtype : tuple_val
                   | dict_val '''
    if isinstance(p[1], list):
        p[0] = tuple(p[1])
    else:
        p[0] = p[1]

def p_tuple_val(p):
    ''' tuple_val : basetype VERTICALBAR
                  | tuple_val basetype VERTICALBAR'''
    if len(p) == 3:
        p[0] = [p[1],]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_dict_val(p):
    ''' dict_val : singlekv VERTICALBAR dict_val
                 | singlekv '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].update(p[3])
        p[0] = p[1]

def p_singlekv(p):
    ''' singlekv : basetype EQUAL basetype '''
    p[0] = {p[1]: p[3]}

def p_error(p):

    if not p:
        raise XlsSyntaxError("值检查语法错误，已到文件末尾")
    else:
        print("Grammar Error", p)

yacc_checker = yacc.yacc(debug=True)
