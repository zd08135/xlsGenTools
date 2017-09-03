# encoding=utf-8

from .type_check_ly import lex_checker, yacc_checker


base_types = [
    int, str, bool, float,
]
def get_type_info(text, logger):
    # print("logger current level", logger.getEffectiveLevel())
    return yacc_checker.parse(text, lexer=lex_checker, debug=logger)

EXISTS = "exists"
UNIQUE = "unique"
DEFAULT = "default"
STAR = "*"

def get_limit_info(limit_str):
    # 这个就不要用ply了
    if limit_str.startswith(EXISTS):
        return (EXISTS,)
    elif limit_str.startswith(UNIQUE):
        return (UNIQUE,)
    elif limit_str.startswith(DEFAULT):
        default_val = limit_str.split("=")[1]
        return (DEFAULT, default_val)
    else:
        return (STAR,)
