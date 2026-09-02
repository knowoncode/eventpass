import hashlib

def encrypt(value):
    result = hashlib.sha256(value.encode())
    result = result.hexdigest()
    return result