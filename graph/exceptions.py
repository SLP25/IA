class InvalidCircuit(Exception):
    """the base exception for circuits errors

    Args:
        Exception (Exception): exc
    """
    pass

class InconsistenceSize(InvalidCircuit):
    """the size of the rows in the matrix are not all the same

    Args:
        InvalidCircuit (InvalidCircuit): exc
    """
    pass

class NoStartsFound(InvalidCircuit):
    """didn't find starts while generating the graph

    Args:
        InvalidCircuit (InvalidCircuit): exc
    """
    pass

class NoFinishesFound(InvalidCircuit):
    """didn't find finishes while generating the graph

    Args:
        InvalidCircuit (InvalidCircuit): exc
    """
    pass


