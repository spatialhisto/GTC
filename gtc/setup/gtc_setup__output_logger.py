#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import sys


class Output_Logger(object):

    """Directly print output to a file and to the terminal.
    Usage:
        import gtc.setup as g_set
        g_set.start_logger('logfile.log')
        print("inside file")
        g_set.stop_logger()
        print("outside file")"""

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a+")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


####


def start_logging(
    file_name: str
):

    """Start transcript, appending print output to given file name."""

    sys.stdout = Output_Logger(file_name)


####


def stop_logging():

    """Stop transcript and return print functionality to normal."""

    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal

#################################
