import os
from time import sleep

if __name__ == "__main__":
    # Get current Path
    cwd = os.getcwd()
    # Start mongod in background
    os.system("mongod -f /etc/mongod.conf &")
    # Start Dfacto in background
    os.system("python3 {call} &".format(call=os.path.join(cwd, "Dfacto.py")))
    # Loop through Ask/Learn/Share
    sleep(10)
    while(True):
        os.system("python3 {call}".format(call=os.path.join(cwd, "DfactoAsk.py")))
        sleep(20)
        os.system("python3 {call}".format(call=os.path.join(cwd, "DfactoLearn.py")))
        sleep(20)
        os.system("python3 {call}".format(call=os.path.join(cwd, "DfactoShare.py")))
        sleep(20)