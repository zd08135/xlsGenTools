
import pickle, hashlib, os
import io, pprint, json

import config, inner_config
import util

pp = pprint.PrettyPrinter(indent=4, width=1)

def dump_dict_to_file(res_dict, output_path, style, logger, \
    gen_variable):
    # print("dump_dict_to_file", pp.pprint(res_dict))
    common_header = util.get_common_header()
    if style == config.STYLE_SINGLE:
        output_path = output_path + util.get_post_fix()
        print ("dump_dict_to_file", output_path)
        ofile = util.open_output_file(output_path)
        util.write_file(ofile, common_header)
        write_version_code(res_dict, ofile, 1)
        util.write_file(ofile, "DATA = \\\n%s\n\n" % pp.pformat(res_dict))

        if gen_variable:
            for k in sorted(res_dict.keys()):
                tbl_name = util.get_table_name(output_path, k)
                util.write_file(ofile, '{tbl} = DATA["{sheet}"]\n'.format(
                    tbl=tbl_name, sheet=k))
        ofile.close()
        return True

    elif style == config.STYLE_SPLIT:
        if os.path.exists(output_path) and not os.path.isdir(output_path):
            logger.error("Should be a directory: %s", output_path)
            return False
        elif not os.path.exists(output_path):
            os.mkdir(output_path)

        init_file_path = util.get_module_file_name()
        init_file = util.open_output_file(os.path.join(output_path, init_file_path))
        util.write_file(init_file, common_header)
        write_version_code(res_dict, init_file, 1)

        for k, data in res_dict.items():
            data_file_path = k
            res = dump_dict_to_file(data, \
                os.path.join(output_path, data_file_path), \
                config.STYLE_SINGLE, logger, False)
            if res == False:
                return False

        if gen_variable:
            for k in sorted(res_dict.keys()):
                tbl_name = util.get_table_name(output_path, k)
                util.write_file(init_file, "from .{sheet} import DATA as {tbl}\n".format(
                    sheet=k, tbl=tbl_name))
            # init_file.write('tbl_{tbl} = DATA["{tbl}"]'.format(tbl=k))
        init_file.close()
        return True
    else:
        logger.error("Invalid style:%s", style)
        return False

def write_version_code(dump_dict, ofile, space_num=0):

    sdata = pickle.dumps(dump_dict)
    m = hashlib.md5(sdata)
    ver = m.hexdigest()
    for _ in range(0, space_num):
        util.write_file(ofile, "\n")
    util.write_file(ofile, "VER = \"%s\"\n" % ver)
    for _ in range(0, space_num):
        util.write_file(ofile, "\n")
