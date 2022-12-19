class GUIException(Exception):
    """base gui exeption

    Args:
        Exception (Exception): exc
    """
    pass

class QUIT(GUIException):
    """exception to quit the application

    Args:
        Exception (GUIException): exc
    """
    pass
class POP(GUIException):
    """exception to go back to the previous view if it exists

    Args:
        Exception (GUIException): exc
    """
    pass
class PERCARVIEW(GUIException):
    """exception to go to the per car view

    Args:
        Exception (GUIException): exc
    """
    pass
class SIMULATIONVIEW(GUIException):
    """exception to go to the simulation view

    Args:
        Exception (GUIException): exc
    """
    pass
class GRAPHVIEW(GUIException):
    """exception to go to the GRAPH view

    Args:
        Exception (GUIException): exc
    """
    pass