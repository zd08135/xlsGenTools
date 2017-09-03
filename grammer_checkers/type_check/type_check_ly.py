# encoding=utf-8
import sys

sys.path.append(
    "..",
)

import re
from grammer_checkers.ply import lex as lex
from grammer_checkers.ply import yacc as yacc

# lexer ------------------------------------
# types and symbols
t_STR = r"str"
t_STRING = r"string"

t_BOOL = r"bool"
t_BOOLEAN = r"boolean"

t_INT = r"int"
t_LONG = r"long"
t_ID = r"id"
t_UID = r"uid"

t_FLOAT = r"float"
t_DOUBLE = r"double"

t_LIST = r"list"
t_TUPLE = r"tuple"
t_DICT = r"dict"

t_VERTICALBAR = r'\|'
t_EQUAL = r"="
# ------------------

reserved = [
    'BOOL', 'BOOLEAN',
    'INT', 'LONG', 'ID', 'UID',
    'FLOAT', 'DOUBLE',
    'STRING', 'STR',
    'LIST', 'TUPLE', 'DICT',
]

tokens = reserved + [
    "VERTICALBAR", "EQUAL",
    # 'NAME',
]


# def t_NAME(t):
#     r'[a-zA-Z_][a-zA-Z_0-9]*'
#     t.type = reserved.get(t.value, 'NAME')
#     return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])

lex_checker = lex.lex(reflags=re.UNICODE)

# parser -----------------
def p_propertytype(p):
    '''propertytype : basetypex
                    | extendtype'''
    p[0] = p[1]

def p_basetypex(p):
    ''' basetypex : basetype '''
    p[0] = (p[1],)

def p_basetype(p):
    ''' basetype : bool_type
                 | int_type
                 | str_type
                 | float_type '''
    p[0] = p[1]

def p_int_type(p):
    ''' int_type : INT
                | LONG
                | ID
                | UID '''
    p[0] = int

def p_str_type(p):
    ''' str_type : STR
                | STRING '''
    p[0] = str

def p_bool_type(p):
    ''' bool_type : BOOL
                  | BOOLEAN '''
    p[0] = bool

def p_float_type(p):
    ''' float_type : FLOAT
                   | DOUBLE '''
    p[0] = float

def p_extendtype(p):
    ''' extendtype : LIST VERTICALBAR basetype
                   | TUPLE VERTICALBAR basetype
                   | DICT VERTICALBAR basetype EQUAL basetype'''
    if p[1] in ["list", "tuple"]:
        p[0] = (tuple, p[3])
    elif p[1] == "dict":
        p[0] = (dict, p[3], p[5])

def p_error(p):

    if not p:
        print(u'类型检查语法错误，已到文件末尾')
        # raise SyntaxError
    else:
        print("Grammar Error", p)

yacc_checker = yacc.yacc(debug=False)
