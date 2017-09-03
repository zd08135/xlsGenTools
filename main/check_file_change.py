
import os, stat

import config

def get_change_file_list(directory, timestamp):
    changed_files = []
    for f in os.listdir(directory):
        real_path = os.path.join(directory, f)
        file_stat = os.stat(real_path)
        if file_stat.ST_MTIME < timestamp:
            changed_files.append(f)
    return changed_files
