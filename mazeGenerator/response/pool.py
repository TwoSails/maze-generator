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
    ok.data = data
    return ok


def ErrResponse(e, data=None) -> Err:
    err.error = e
    err.data = data
    return err
