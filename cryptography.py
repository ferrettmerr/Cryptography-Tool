def shift(message, shift, decrypt = False, alpha = 'abcdefghijklmnopqrstuvwxyz'):
    
    shift %= len(alpha)
    if decrypt:
        shift = len(alpha) - shift
    trans = dict([(alpha[i], alpha[(i + shift) % 26]) for i in range(26)])
    outstring = ''

    for a in message:
        if trans.has_key(a.lower()):
            if a.islower():
                outstring += trans[a]
            else:
                outstring += trans[a.lower()].upper()
        else:
            outstring += a

    return outstring

def affine(message, a, b, decrypt = False):
    
    return "not implemented"

def substitution(message, substitutions, decrypt = False):
    
    return "not implemented"

def permutation(message, block_size, swaps, decrypt = False):
    
    return "not implemented"

def vigenere(message, key, decrypt = False, strip = False):
    """
    vigenere(message, key, decrypt = False, strip = False)
    
    Encrypts or decrypts a message using the Vigenere cipher.
    If strip is True, all non-alphabetic characters are stripped from the
    message, and it is converted to lower case.
    """
    if strip:    # Strip whitespace and punctuation
        message = filter(str.isalpha, message).lower()

    key = filter(str.isalpha, key).lower()

    alpha = 'abcdefghijklmnopqrstuvwxyz'
    tonum = dict([(alpha[i], i) for i in range(len(alpha))])

    # Construct the tabula recta
    lookup = dict([(a, 0) for a in alpha])
    for a in lookup:
        if not decrypt:
            lookup[a] = dict([(b, alpha[(tonum[a] + tonum[b]) % 26]) for b in alpha])
        else:
            lookup[a] = dict([(b, alpha[(tonum[a] - tonum[b]) % 26]) for b in alpha])
    
    out = ''
    for i in range(len(message)):
        if message[i].isalpha():
            letter = lookup[message[i].lower()][key[i % len(key)]]
            if message[i].isupper():
                out += letter.upper()
            else:
                out += letter
        else:
            out += message[i]

    return out

def one_time_pad(message, key, decrypt = False):
    
def hill(message, key, decrypt = False):
    
    from math import sqrt
    n = int(sqrt(len(key)))
    if n * n != len(key):
        raise Exception("Invalid key length")
    
    message = filter(str.isalpha, message).lower()
    
    #alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,?!:;()1234567890'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    tonum = dict([(alpha[i], i * 1.) for i in range(len(alpha))])

    # Construct our key matrix
    keylist = []
    for a in key:
        keylist.append(tonum[a])
    keymatrix, inverse = [], []
    for i in range(n):
        keymatrix.append(keylist[i * n:i * n + n])
        inverse.append(keylist[i * n:i * n + n])
    
    # Make sure the key matrix is invertible, use the inverse if decrypting
    try:
        #inverse = matrix_invert(inverse)
        pass
    except Exception:
        raise Exception("Uninvertible key matrix")
    if decrypt:
        raise Exception("Decryption not supported.") # To remove once we have an inversion function
        keymatrix = inverse

    # Pad the message with spaces^WAs if necessary
    if len(message) % n > 0:
        message += ' ' * (n - (len(message) % n))

    # Main loop
    from string import join
    out = ''
    for i in range(len(message) / n):
        lst = [[tonum[a]] for a in message[i * n:i * n + n]]
        lst = [[sum(i * j for i, j in zip(row, col)) for col in zip(*lst)] for row in keymatrix]
        out += ''.join([alpha[int(lst[j][0]) % len(alpha)] for j in range(len(lst))])
    
    return out