class Math:
    def lerp(X1: float, X2: float, X3: float, Y1: float, Y2: float) -> float:
        return ((X2 - X3) * Y1 + (X3 - X1) * Y2) / (X2 - X1)
