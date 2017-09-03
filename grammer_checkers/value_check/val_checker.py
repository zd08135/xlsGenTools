# encoding=utf-8

from grammer_checkers.ply.lex import LexError
from util import XlsSyntaxError
from .val_check_ly import lex_checker, yacc_checker

def get_real_val(cell_value, type_info, logger):
    real_value = None
    try:
        real_value = yacc_checker.parse(str(cell_value), lexer=lex_checker, debug=logger)
    except LexError as lexe:
        print(list_errors_info())
        error_content = "error when parsing %s with type(%s): %s" % \
            (str(cell_value), str(type_info), str(lexe))
        print(error_content)
        logger.error(error_content)
    except XlsSyntaxError as xlse:
        print(list_errors_info())
        error_content = "error when parsing %s with type(%s): %s" % \
            (str(cell_value), str(type_info), str(xlse))
        print(error_content)
        logger.error(error_content)
    finally:
        if not isinstance(real_value, type_info[0]):
            logger.error("type not matched: %s(%s)-%s", cell_value, \
                real_value, str(type_info))
            return None
        return real_value

def list_errors_info():
    from .val_check_ly import t_VERTICALBAR
    infos = "\n".join([
        "语法检查出错，可能有以下原因：",
        "1. 字符串前后没有加引号，包括字符串定义，和tuple/list，以及dict的(key,value)中用到的字符串",
        "2. list, tuple的最后一个字符一定是%s" % (t_VERTICALBAR[-1]),
        ])
    return infos
