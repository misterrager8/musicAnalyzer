# TODO:
# [ ]WebView(?)
# [ ]Pandas implem. for data analysis
# [ ]Testing

import os
import subprocess
import sys

from modules import CLview

if __name__ == "__main__":
    if sys.argv[1] == "cl":
        CLview.HomePrompts()
    elif sys.argv[1] == "dt":
        path = os.getcwd() + "/modules"
        os.chdir(path)
        subprocess.call("/Users/chemlleijoseph/jython2.7.1/bin/jython GUIview.py", shell=True)
