import shutil

from paths import APP_DIR
from configuration import read_config
config = read_config()


def disk_usage():
    '''
    BRO
    Returns disk usage in bytes in a form of a list (total, used, free)
    '''
    return shutil.disk_usage(APP_DIR)

def human_readable_bytes(num, suffix='B'):
    '''
    BRO
    Converts bytes into
    '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

