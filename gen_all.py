# encoding=utf-8

import os, sys
import config, inner_config
import tracebackturbo
import util

sys.path.append(".grammer_checkers")
sys.path.append("./grammer_checkers/ply")
sys.path.append("./grammer_checkers/type_check")
sys.path.append("./grammer_checkers/value_check")
sys.path.append("./openpyxl")
sys.path.append(config.SRC_DIR)

import main.main as main_entry

# import inner_config

# 任何地方执行，都会切换到本文件所在目录
PWD = os.path.split(os.path.realpath(__file__))[0]
os.chdir(PWD)
print("运行目录: ", os.getcwd())

def main(args):

    filter_type = args[1]
    file_list = get_transfer_file_list(filter_type)
    if not file_list:
        print("无文件变化，未生成内容")
        return
    main_entry.real_process(file_list)

def get_transfer_file_list(filter_type="ALL"):
    file_list = []
    for k in os.listdir(config.XLS_DIR):
        if k not in config.GEN_DICT:
            continue
        if filter_type == "ALL":
            file_list.append(k)
        elif filter_type == "INC":
            if not main_entry.check_target_latest(k, config.GEN_DICT[k]):
                file_list.append(k)

    return file_list

tracebackturbo.install_traceback()
if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(tracebackturbo.print_exc())
