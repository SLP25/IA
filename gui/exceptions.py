class QUIT(Exception):
    """exception to quit the application

    Args:
        Exception (Exception): exc
    """
    pass
class POP(Exception):
    """exception to go back to the previous view if it exists

    Args:
        Exception (Exception): exc
    """
    pass
class PERCARVIEW(Exception):
    """exception to go to the per car view

    Args:
        Exception (Exception): exc
    """
    pass
class SIMULATIONVIEW(Exception):
    pass