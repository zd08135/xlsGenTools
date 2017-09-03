# encoding=utf-8
# check_functions

import os
import config

def check_xls_in(sheet1, col1, sheet2, col2):

    msgs = []
    col2_values = {}
    if col2 == "id":
        col2_values = sheet2.keys()
    else:
        for k2, v2 in sheet2.items():
            col_v = v2.get(col2, None)
            if col_v:
                col2_values[col_v] = True
    for k1, v1 in sheet1.items():
        if col1 not in v1:
            continue
        col_v = v1[col1]
        if col_v not in col2_values:
            msgs.append("%s, %s check error" % (str(k1), str(v1)))
    return msgs

def check_res_exist(sheet1, col1, res_path):

    msgs = []
    parent_path = os.path.join(".", res_path)
    for k, v in sheet1.items():
        if col1 not in v:
            msgs.append("%s %s check error: xls error" % (k, col1))
            continue
        col_v = v[col1]
        real_path = os.path.join(parent_path, col_v)
        if os.path.isfile(real_path) and os.access(real_path, os.R_OK):
            pass
        else:
            msgs.append("%s %s check error: file not exist" % (k, col1))
    return msgs
'''
dungeon.battle.instance xls_in dungeon.instance.id
dungeon.monster.model_path res_exists "res\model"

def check_func_1():
    from gen import xls_dungeon
    check_xls_in(xls_dungeon.tbl_dungeon_battle, "instance", \
        xls_dungeon.tbl_dungeon_instance, "id")

def check_func_2():
    from gen import xls_dungeon
    check_res_exist(xls_dungeon.tbl_dungeon_monster, "model_path", "res\model")
'''
