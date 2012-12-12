def shift(message, shift, decrypt = False, alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    
    shift %= len(alpha)
    if decrypt:
        shift = len(alpha) - shift
    trans = dict([(alpha[i], alpha[(i + shift) % 26]) for i in range(26)])
    outstring = ''

    for a in message:
        if trans.has_key(a):
            if a:
                outstring += trans[a]
            else:
                outstring += trans[a].upper()
        else:
            outstring += a

    return outstring

def affine(message, a, b, decrypt = False, alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):

    VALUES = dict(zip(alpha, range(len(alpha))))
    RVALUES = dict(zip(range(len(alpha)), alpha))
    text = ""

    if (decrypt):
        m = find_coprime(a)
        text = [ RVALUES[(m * (VALUES[i] - b)) % 26] for i in message ]
    else:
        text = [ RVALUES[(a * VALUES[i] + b) % 26] for i in message ]

    return ''.join(text)

def find_coprime(a):

    for i in range(26):
        if ((i * a) % 26) == 1:
            return i
        
    #Raise an error
    raise Exception, "The codeword %d has not a coprime, try another" % a
    

def substitution(message, substitutions, decrypt = False):
    
    new_message = ""
    for char in message:
        if (char in substitutions):
            new_message += substitutions[char]
    

    return new_message

def permutation(message, cipher, decrypt = False):
    message = "".join(message.split(" ")).upper()
    ciphertext = ""
    
    if decrypt:
        cipher = inverse_key(cipher)

    for pad in range(0, len(message) % len(cipher) * - 1 % len(cipher)):
        message += "X"
    
    for offset in range(0, len(message), len(cipher)):
        for element in cipher:
            ciphertext = ciphertext + message[offset + element -1]
    
    return ciphertext

def inverse_key(cipher):
    inverse = []
    for position in range(min(cipher),max(cipher)+1,1):
        inverse.append(cipher.index(position)+1)
    return inverse

def vigenere(message, key, decrypt = False):
    """
    vigenere(message, key, decrypt = False, strip = False)
    
    Encrypts or decrypts a message using the Vigenere cipher.
    If strip is True, all non-alphabetic characters are stripped from the
    message, and it is converted to lower case.
    """

    key = filter(str.isalpha, key)

    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
            letter = lookup[message[i]][key[i % len(key)]]
            if message[i].isupper():
                out += letter.upper()
            else:
                out += letter
        else:
            out += message[i]

    return out

def one_time_pad(message, key, decrypt = False):

    startchar = 'A'
    endchar = 'Z'
    modular = 26

    if len(key) < len(message):
        return "ERROR: KEY NOT LONG ENOUGH"

    if not decrypt:  
        #encyrpt  
        ret = ""
        for i in range(len(message)):
            messagechar = ord(message[i]) - ord(startchar)
            keychar = ord(key[i]) - ord(startchar)
            calculatedchar = (messagechar + keychar) % modular
            convertedchar = chr(calculatedchar + ord(startchar))
            ret += convertedchar
        return ret
    else:
        #decrypt
        ret = ""
        for i in range(len(message)):
            messagechar = ord(message[i]) - ord(startchar)
            keychar = ord(key[i]) - ord(startchar)
            calculatedchar = (messagechar - keychar) % modular
            convertedchar = chr(calculatedchar + ord(startchar))
            ret += convertedchar
        return ret
    
def hill(message, key, decrypt = False):
    
    from math import sqrt
    n = int(sqrt(len(key)))
    if n * n != len(key):
        raise Exception("Invalid key length")
    
    message = filter(str.isalpha, message).upper()
    
    #alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,?!:;()1234567890'
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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