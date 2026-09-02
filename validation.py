
def empty(dataList):
    for d in dataList:
        if d=='':
            return True
    return False


def checkAlpha(dataList):
    for d in dataList:
        if not d.isalpha():
            return True
    return False

def checkDigit(dataList):
    for d in dataList:
        if not d.isdigit():
            return True
    return False