import sys
input = sys.stdin.readline
from performance_checker import PerformanceChecker

MODULA = 1_000_000_000 + 7
N, K = map(int, input()[:-1].split())


p_checker = PerformanceChecker()
p_checker.start()

# f(n, k)값을 저장하는 dp
# k^n을 저장하는 pows
# 소수판별을 위한 primes
dp, pows, prime_status = [0] * (N+1), [-1] * (N+1), [True] * (N+1)
dp[1] = (K**2) % MODULA
pows[0] = 1
pows[1] = K
primes = []

# primes 초기화
for i in range(2, N+1):
    if prime_status[i]:
        primes.append(i)
        for j in range(i+i, N+1, i):
            prime_status[j] = False

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
    
def modular_div(a, b):
    # 모듈러 나누기 연산
    return (((MODULA+1)/b) * a) % MODULA

def f(n, k):
    prev_ans, p = 0, 0

    if n == 1:
        return k**2

    for prime in primes:
        if n % prime == 0:
            p = n//prime
            prev_ans = f(p, k)
            break
    
    ans = 1
    if p == 1:
        for i in range(0, n):
            ans = (ans * (get_pow(k, 2) - i)) % MODULA
    else:
        for i in range(0, n//p):
            ans = (ans * (get_pow(k, p*2) - i)) % MODULA

    ans = int(modular_div(ans, n))
    ans = (ans + prev_ans) % MODULA

    return ans

print(f(N, K))
p_checker.stop()
p_checker.print()