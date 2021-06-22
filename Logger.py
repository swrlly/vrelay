import os
import re
import sys

class Logger:

    path = "logs/"


    def openLogFile(self):

        # check next
        allLogs = os.listdir(self.path)
        log = None
        if allLogs == []:
            log = open(self.path + "aoelog 0.txt", "a")
        else:
            num = 0
            for l in allLogs:
                logNumber = int(re.search('\s([0-9]+)', l).group(0))
                num = max(num, logNumber + 1)
            log = open(self.path + "aoelog {}.txt".format(num), "a")
            

        sys.stdout = log
               
