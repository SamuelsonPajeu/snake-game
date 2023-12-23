class Error(Exception):
    pass

class GameOver(Exception):
    pass

def nil() -> tuple[None, None]:
    return (None, None)