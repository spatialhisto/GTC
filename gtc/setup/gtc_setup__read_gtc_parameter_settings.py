#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import ast
import sys


def read_gtc_parameter_settings(
    fname_gtc_param: str
) -> dict:

    """Read in settings from gtc parameters file
    and convert parameters into dictionary."""

    param_file = open(fname_gtc_param, 'r')
    file_content = param_file.read()  # read in file content of text file

    try:
        p = ast.literal_eval(file_content)  # create dictionary from file content

    except ValueError as ex:
        _exc_type, exc_value, exc_traceback = sys.exc_info()
        print("ERROR: %r" % (exc_value))
        # traceback.print_tb(exc_traceback)
        last_tb = exc_traceback
        while last_tb.tb_next:
            last_tb = last_tb.tb_next
        print("Error in file: %s" % fname_gtc_param)
        print("Error location: line=%d, col=%d" % (
            last_tb.tb_frame.f_locals["node"].lineno,
            last_tb.tb_frame.f_locals["node"].col_offset))

    return p


#################################
