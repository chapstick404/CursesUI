class Logger():
    def __init__(self, loglevel=0):
        self.log_level = loglevel
        logfile = open("log.txt", "w")
        logfile.close()

    def log(self, *logstrings):
        if self.log_level < 1:
            return
        with open("log.txt", "a") as logfile:
            logfile.write(logstrings[0])
            logfile.write("\n")
            if self.log_level > 1:
                for logindex in range(1, self.log_level):
                    if logindex < len(logstrings):
                        logfile.write(logstrings[logindex])
                        logfile.write("\n")
