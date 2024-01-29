def spot_marked_x(s: str = "[rh<c8^ey?}ng:el") -> str:
    return "".join(chr(ord(c) ^ 11) for c in s)

print(spot_marked_x())