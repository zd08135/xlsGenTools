

import os, shutil

POSTFIX = [".xls", ".xlsx"]

TBL_MAP = {
    "tbl": "dungeon"
}

COPY_TIMES = 200

filelist = {}
for fname in os.listdir("."):
    for pfx in POSTFIX:
        if fname.endswith(pfx):
            no_pfx_fname = fname[:-len(pfx)]
            filelist[no_pfx_fname] = pfx

for no_pfx_fname, pfx in filelist.items():
    xls_name = TBL_MAP.get(no_pfx_fname)
    if not xls_name:
        continue
    filepath = os.path.join(".", no_pfx_fname + pfx)
    for i in range(1, COPY_TIMES):
        outname = no_pfx_fname + str(i) + pfx
        out_xls_name = xls_name + str(i)
        outpath = os.path.join(".", outname)
        shutil.copy(filepath, outpath)
        print('"%s": "%s",' % (outname, out_xls_name))
