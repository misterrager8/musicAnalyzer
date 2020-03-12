import sys
from modules import model, CLview
import subprocess
import os
      
if __name__ == "__main__":
  if sys.argv[1] == "cl":
    CLview.homePrompts()
  elif sys.argv[1] == "dt":
    path = os.getcwd() + "/modules"
    os.chdir(path)
    subprocess.call("/Users/chemlleijoseph/jython2.7.1/bin/jython GUIview.py", shell = True)