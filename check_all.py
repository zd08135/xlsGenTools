# encoding=utf-8

import io
import config
import util

def dump_check_code(output_path):
    ofile = util.open_output_file(output_path)
    xls_in_rules = config.CHECK_RULES["XLSIN"]
    res_exist_rules = config.CHECK_RULES["RESEXIST"]
    util.write_file(ofile, util.get_common_header())
    code = \
    """from grammer_checkers.check_functions import check_xls_in\n""" \
    """from grammer_checkers.check_functions import check_res_exist\n\n"""
    util.write_file(ofile, code)
    idx = 0
    func_names = {}
    for rule in xls_in_rules:
        idx += 1
        rule_desc = rule[-1]
        func_name = gen_check_code_xls_in(ofile, rule, idx)
        func_names[func_name] = '"%s"' % rule_desc
    for rule in res_exist_rules:
        idx += 1
        rule_desc = rule[-1]
        func_name = gen_check_code_res_exist(ofile, rule, idx)
        func_names[func_name] = '"%s"' % rule_desc

    # print("func_names", func_names)

    code = """funcs = {\n"""
    util.write_file(ofile, code)
    codes = []
    for func, rule_desc in func_names.items():
        codes.append("    {func}: {rule},".format(func=func, rule=rule_desc))
    codes.append("}\n")
    util.write_file(ofile, "\n".join(codes))
    code = \
    """def real_check():\n""" \
    """    for func, rule_desc in funcs.items():\n""" \
    """        msgs = func()\n""" \
    """        if msgs:\n""" \
    """            print("Check Error:", rule_desc)\n""" \
    """            print("Info:")\n""" \
    """            print("\\n".join(msgs))\n\n""" \
    """if __name__ == "__main__":\n""" \
    """    real_check()"""
    util.write_file(ofile, code)
    ofile.close()

def gen_check_code_xls_in(ofile, rule, idx):
    t1, col1 = rule[0]
    t2, col2 = rule[1]

    py1, sh1 = t1.split(".")
    py1 = config.GEN_FILE_FRONT + py1
    s1 = util.get_table_name(py1, sh1)

    py2, sh2 = t2.split(".")
    py2 = config.GEN_FILE_FRONT + py2
    s2 = util.get_table_name(py2, sh2)

    function_name = "check_xls_rule_%d" % idx
    code = \
    """def {func_name}():\n""" \
    """    from {src_dir} import {wb1}\n""" \
    """    from {src_dir} import {wb2}\n""" \
    """    return {inner_func_name}({tbl1},"{col1}",{tbl2},"{col2}")\n\n""".format(
        func_name=function_name, src_dir=config.SRC_DIR,
        wb1=py1, wb2=py2,
        tbl1=".".join([py1, s1]), tbl2=".".join([py2, s2]),
        col1=col1, col2=col2,
        inner_func_name="check_xls_in"
    )
    util.write_file(ofile, code)
    return function_name

def gen_check_code_res_exist(ofile, rule, idx):
    t1, col1, res_path = rule[0]
    py1, sh1 = t1.split(".")
    py1 = config.GEN_FILE_FRONT + py1
    s1 = util.get_table_name(py1, sh1)

    function_name = "check_res_exist_%d" % idx
    code = \
    """def {func_name}():\n""" \
    """    from {src_dir} import {wb1}\n""" \
    """    return {inner_func_name}({tbl1},"{col1}","{respath}")\n\n""".format(
        func_name=function_name, src_dir=config.SRC_DIR,
        wb1=py1, tbl1=".".join([py1, s1]), col1=col1, respath=res_path,
        inner_func_name="check_res_exist",
    )
    util.write_file(ofile, code)
    return function_name
