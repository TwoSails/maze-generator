"""
Initialises objects which can be referenced to save execution time initialising objects.
"""
from mazeGenerator.response.exceptions import TileNameNotSet, TileDoesNotExist, InvalidEdgeLabel, InvalidResolution, \
    ExceedsBounds, EmptyBoard, TileSetDoesNotExist, InvalidState, TileNotActive, \
    TileSetNameNotSet
from mazeGenerator.response import Ok, Err

TileNameNotSetErr = Err(TileNameNotSet)
TileDoesNotExistErr = Err(TileDoesNotExist)
InvalidEdgeLabelErr = Err(InvalidEdgeLabel)
InvalidResolutionErr = Err(InvalidResolution)
ExceedsBoundsErr = Err(ExceedsBounds)
EmptyBoardErr = Err(EmptyBoard)
TileSetDoesNotExistErr = Err(TileSetDoesNotExist)
InvalidStateErr = Err(InvalidState)
TileNotActiveErr = Err(TileNotActive)
TileSetNameNotSetErr = Err(TileSetNameNotSet)

ok = Ok()
err = Err()


def OkResponse(data) -> Ok:
    """
    Used to set data for response object to be referenced
    Use of this method improves performance
    """
    ok.data = data
    return ok


def ErrResponse(e, data=None) -> Err:
    """
    Used to set data and error for response object to be referenced
    """
    err.error = e
    err.data = data
    return err
