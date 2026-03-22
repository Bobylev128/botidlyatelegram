def validate_rounds(text, total):
    try:
        nums = list(map(int, text))
    except:
        return False

    res = 1
    for n in nums:
        res *= n

    return res == total