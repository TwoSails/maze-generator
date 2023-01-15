from typing import Any


def NoneTypeCheck(arg, null: Any = 0):
    if arg is None:
        return null

    return arg
