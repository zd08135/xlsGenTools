# encoding=utf-8
'''This File is generated By xlsGenTools'''
# pylint: disable=C0326, C0103, C0111


GEN_TIME=1504190099
GEN_USER="e6444f487dfe7117ef45b22e418c17306c795a79dcc77419a2df020054ce59446e83227aa52105d952ef651e2b43b7a55bf97224363bef8dcde058e462fce859"

from grammer_checkers.check_functions import check_xls_in
from grammer_checkers.check_functions import check_res_exist

def check_xls_rule_1():
    from gen import xls_dungeon
    from gen import xls_dungeon
    return check_xls_in(xls_dungeon.tbl_dungeon_tables,"instance",xls_dungeon.tbl_dungeon_instance,"id")

def check_xls_rule_2():
    from gen import xls_dungeon
    from gen import xls_dungeon
    return check_xls_in(xls_dungeon.tbl_dungeon_tables,"instance",xls_dungeon.tbl_dungeon_instance,"id")

def check_res_exist_3():
    from gen import xls_dungeon
    return check_res_exist(xls_dungeon.tbl_dungeon_tables,"model_path","res/model")

funcs = {
    check_xls_rule_1: "副本battle表的instance属于副本instance表key",
    check_xls_rule_2: "副本battle表的instance属于副本instance表key",
    check_res_exist_3: "副本怪物表中怪物的model_path必须存在于res/model目录下",
}
def real_check():
    for func, rule_desc in funcs.items():
        msgs = func()
        if msgs:
            print("Check Error:", rule_desc)
            print("Info:")
            print("\n".join(msgs))

if __name__ == "__main__":
    real_check()