#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################


def quote(
    text: str
) -> str:

    """Set quotation marks inside string (quotation marks)."""

    return ('\'%s\'' % text)


####


def convert_list_to_string(
    gene_list: list
) -> str:

    """Set quotation marks inside string (quotation marks)."""

    sep = '-'

    return sep.join(map(str, gene_list))

#################################
