import itertools

n,q = 128, 256
P.<x> = PolynomialRing(Zmod(q))
Q.<y> = P.quotient(x^n+1)

def prod(a,b):
    # nothing to see here ;)
    return Q([aa*bb for aa,bb in zip(a,b)])

def sample():
    v = []
    for i in range(n):
        v.append(randrange(-2,3))
    return Q(v)

def encode(u):
    def s2bits(s):
        return list(itertools.chain(*[[int(b) for b in bin(ord(c))[2:].zfill(8)] for c in s]))
    return Q([q//2 if uu == 1 else 0 for uu in s2bits(u)])

def decode(v):
    def bits2s(bits):
        return "".join([chr(int("".join([str(b) for b in bits[i:i+8]]),2)) for i in range(0,len(bits),8)])
    return bits2s([0 if ZZ(vv-q//4) > q//2 else 1 for vv in v])

def gen():
    a = Q.random_element()
    s = sample()
    e = sample()
    b = prod(a,s) + e
    return (b,a),s

def E(m,pk):
    b,a = pk
    t = sample()

    e = sample()
    u = prod(a,t) + e

    e = sample()
    v = prod(b,t) + e + m
    return u,v

def D(c,sk):
    u,v = c
    s = sk
    return v - prod(u,s)

pk,sk = gen()
k = os.urandom(16)
c = E(encode(k),pk)
assert decode(D(c,sk)) == k
