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
    
def hill(message, matrix, encryption = False):

    import utils

    if not utils.invertible(matrix):
        # The matrix should be invertible.
        return "Non invertible matrix"
    if len(message) % 2 != 0:
        message = message + 'X'
    couple = [list(message[i*2:(i*2)+2]) for i in range(0, len(message)/2)]
    result = [i[:] for i in couple]
    if not encryption:
        # To decrypt, just need to inverse the matrix.
        matrix = utils.inverse_matrix(matrix)
    for i, c in enumerate(couple):
        if c[0].isalpha() and c[1].isalpha():
            result[i][0] = chr(((ord(c[0])-65) * matrix[0][0] + \
                                    (ord(c[1])-65) * matrix[0][1]) % 26 + 65)
            result[i][1] = chr(((ord(c[0])-65) * matrix[1][0] + \
                                    (ord(c[1])-65) * matrix[1][1]) % 26 + 65)
    return "".join(["".join(i) for i in result])