# encoding=utf-8

import os, sys, time
import concurrent.futures, multiprocessing, importlib
from . import xls2py
import config, inner_config
import util
import tracebackturbo

def real_process(file_list):
    print(file_list)
    make_src_module()
    converters = []
    for k in file_list:
        if k not in config.GEN_DICT:
            continue
        out = config.GEN_DICT[k]
        input_path = os.path.join(config.XLS_DIR, k)
        output_path = os.path.join(config.SRC_DIR, config.GEN_FILE_FRONT + out)
        converter = xls2py.XlsConverter(input_path, output_path, config.OUTPUT_STYLE)
        converters.append(converter)

    start_time = time.clock()
    if inner_config.RUN_STYLE == inner_config.SEQUENCE_RUN:
        for converter in converters:
            converter.convert()
    elif inner_config.RUN_STYLE == inner_config.PARALLEL_RUN:
        try:
            print("cpu num", multiprocessing.cpu_count())
            with concurrent.futures.ProcessPoolExecutor(\
                max_workers=inner_config.PARALLEL_WORK_NUM) as executor:
                for converter in converters:
                    executor.submit(covert_task, converter)
        except Exception as ex:
            print(tracebackturbo.print_exc())

    end_time = time.clock()
    print ("time: start=%s, end=%s, cost=%s" % (start_time, end_time, end_time - start_time))

    gen_check_code()

def make_src_module():
    if not os.path.exists(config.SRC_DIR):
        os.mkdir(config.SRC_DIR)
    module_path = os.path.join(config.SRC_DIR,
        util.get_module_file_name())
    util.open_output_file(module_path).close()

def gen_check_code():
    from check_all import dump_check_code
    check_file = os.path.join(config.CHECK_CODE_FILE)
    dump_check_code(check_file)

def covert_task(_converter):
    _converter.convert()

def check_target_latest(input, out):
    # 1: 目标存在
    # 2: 上一次生成作者是自己
    # 3：源文件修改时间小于目标生成时间
    # 同时满足以上条件认为是最新的，不需要重新生成
    input_path = os.path.join(config.XLS_DIR, input)
    file_stat = os.stat(input_path)
    output_path = os.path.join(config.SRC_DIR, config.GEN_FILE_FRONT + out)
    if not os.path.exists(output_path):
        return False
    output_path = output_path.replace(os.sep, ".")
    module = importlib.import_module(output_path)
    last_gen_time, last_gen_user = module.GEN_TIME, module.GEN_USER
    return util.get_user() == last_gen_user and \
        last_gen_time > file_stat.st_mtime
