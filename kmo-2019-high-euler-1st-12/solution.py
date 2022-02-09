import sys
input = sys.stdin.readline
MODULA = 1_000_000_000 + 7
N, K = map(int, input()[:-1].split())

# f(n, k)값을 저장하는 dp
# k^n을 저장하는 pows
# 소수판별을 위한 primes
dp, pows, primes = [0] * (N+1), [-1] * (N+1), [True] * (N+1)
dp[1] = (K**2) % MODULA
pows[0] = 1
pows[1] = K

# primes 초기화
for i in range(2, N+1):
    if primes[i]:
        for j in range(i+i, N+1, i):
            primes[j] = False

def get_divisors(n):
    # 약수 구하기, 단 n은 제외한다.
    m = int(n**0.5)
    res = set({1})
    
    if primes[n]:
        # 소수인 경우 패스
        return res

    for i in range(2, m+1):
        if n%i == 0:
            res.add(i)
    new_v = set()
    for v in res:
        if v > 1:
            new_v.add(n//v)
    res.update(new_v)

    return res

def get_pow(r, n):
    # r: 밑, n: 지수
    if pows[n] > 0:
        return pows[n]
    v = get_pow(r, n//2)
    if n%2 == 0:
        pows[n] = (v * v) % MODULA
    else:
        pows[n] = (((v * v) % MODULA) * r) % MODULA
    return pows[n]
    

def f(n, k):
    
    ans = 0
    if dp[n] > 0:
        # 이미 값이 저장되어 있는 경우
        return dp[n]
    
    divs, j = list(get_divisors(n)), 0
    j = n if primes[n] else max(divs)
    
    while divs:
        f(divs.pop(), k)

    tmp = 1
    for i in range(0, j):
        tmp = (tmp * (get_pow(k, n) - i)) % MODULA
    tmp = tmp // n

    dp[n] = (tmp + ans) % MODULA
    return dp[n]

f(N, K)
divs = get_divisors(N)
ans = 0
for a in divs:
    ans = (ans + dp[a]) % MODULA
ans = (ans + dp[N]) % MODULA

print(ans)