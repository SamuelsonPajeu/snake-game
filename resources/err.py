class Error(Exception):
    pass

def nil() -> tuple[None, None]:
    return (None, None)