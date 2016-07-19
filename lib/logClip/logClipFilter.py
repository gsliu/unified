import re


def kbLogFilter(log):
    #regex = r'^(0x){0,1}[a-f0-9-]+$' 
    regex = r'^((guid-)|(0x){0,1})[a-f0-9-]+$' 
    pattern = re.compile(regex)
    match = pattern.search(log)
    if match:
        return ""
    else:
        return log
