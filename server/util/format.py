def tryAsIntOr(value : str, default : int):
    try:
        return int(value)
    except:
        return default