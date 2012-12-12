#!/usr/bin/env python
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VALUES = dict(zip(LETTERS, range(len(LETTERS))))
RVALUES = dict(zip(range(len(LETTERS)), LETTERS))

def find_coprime(a):
    """
    >>> find_coprime( 5 )
    21
    >>> find_coprime( 21 )
    5

    """
    for i in range(26):
        if ((i * a) % 26) == 1:
            return i
        
    #Raise an error
    raise Exception, "The codeword %d has not a coprime, try another" % a

def encode_affine(msg, a, b):
    """
    >>> encode_affine('PROGRAMMINGPRAXIS', 5, 8)
    'FPAMPIQQWVMFPITWU'
    """
    
    #Code to numbers
    encoded_message = [ RVALUES[(a * VALUES[i] + b) % 26] for i in msg ]
        
    return ''.join(encoded_message)


def decode_affine(msg, a, b):
    """
    >>> decode_affine('FPAMPIQQWVMFPITWU', 5, 8)
    'PROGRAMMINGPRAXIS'
    """
    #Inverse of the modulo
    m = find_coprime(a)
    
    decoded_message = [ RVALUES[(m * (VALUES[i] - b)) % 26] for i in msg ]
    
    return ''.join(decoded_message)


if __name__ == '__main__':    
    import doctest
    doctest.testmod()