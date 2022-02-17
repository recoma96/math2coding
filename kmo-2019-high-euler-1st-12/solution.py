import sys
input = sys.stdin.readline
from performance_checker import PerformanceChecker

MODULA = 1_000_000_000 + 7
N, K = map(int, input()[:-1].split())

p_checker = PerformanceChecker()
p_checker.start()

# f(n, k) 저장 dp, 제곱 dp, 약수 dp
dp, pows, divisors = [0] * (N+1), [-1] * (N+1), []
dp[1] = (K**2) % MODULA
pows[0] = 1
pows[1] = K**2 # 제곱 밑은 k가 아닌 k**2다

def get_divisors(n):
    # n의 약수 구하는 알고리즘
    i = 1
    while i <= n**0.5:
        if n % i == 0:
            divisors.append(i)
        i += 1
    i = len(divisors) - 1
    while i >= 0:
        r = n // divisors[i]
        if r != divisors[i]:
            divisors.append(r)
        i -= 1

def get_pow(n):
    # 제곱 구하는 알고리즘
    # r: 밑, n: 지수
    if pows[n] > 0:
        return pows[n]
    v = get_pow(n//2)
    if n%2 == 0:
        pows[n] = (v * v) % MODULA
    else:
        pows[n] = (((v * v) % MODULA) * (K**2)) % MODULA
    return pows[n]
    
def modular_div(a, b):
    # 페르마의 소정리를 이용한 모듈러 나눗셈
    def __pow(r, n):
        if n == 1:
            return r
        else:
            v = __pow(r, n>>1)
            if n%2==0:
                return (v * v) % MODULA
            else:
                return (v * v * r) % MODULA
        
    # 모듈러 나누기 연산
    rev_b = __pow(b, MODULA-2)
    return (a * rev_b) % MODULA

def modular_sub(a, b):
    # 모듈러 뺄샘
    ans = a - b
    if ans < 0:
        ans += MODULA
    return ans

def f(n, k):
    # 바람개비의 모든 날개들이 규칙성을 가지지 않는 경우
    if dp[n] > 0:
        # 이미 연산되어있으면 리턴
        return dp[n]
    
    # n개의 날개에 칠할 수 있는 모든 경우
    ans = get_pow(n)

    # 자신을 제외한 나머지 약수 연산
    subtask_sum = 0
    for divs in divisors:
        if n % divs == 0 and n != divs:
            subtask_sum = (subtask_sum + (divs * f(divs, k) % MODULA)) % MODULA
    
    ans = modular_div(modular_sub(ans, subtask_sum), n)
    dp[n] = ans
    return ans

def s(n, k):
    # 최종합
    get_divisors(n)
    f(n, k)

    ans = 0
    for divs in divisors:
        ans = (ans + dp[divs]) % MODULA

    return ans

# run process
print(s(N, K))

p_checker.stop()
p_checker.print()