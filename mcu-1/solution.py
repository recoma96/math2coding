import math
import collections

a = input().split()
q1, q2 = collections.deque(), collections.deque()
failed, use_div = False, False

for char in a[0]:
    # 맨 앞의 값 불러오기
    q1.append(int(char))

for i in range(1, len(a), 2):

    c = a[i] # 연산자

    # 피연산자 불러오기
    for char in a[i+1]:
        q2.append(int(char))

    if c == '+':
        # 더하기
        while q2:
            q1.append(q2.popleft())
        while q1 and q1[0] == 0:
            q1.popleft()

    elif c == '-':
        # 빼기

        if len(q1) < len(q2):
            # q2의 길이가 더 길면 교체
            q1, q2 = q2, q1
        
        for i in range(len(q1) - 1, -1, -1):
            # 일의 자리부터 차례대로 계산
            if not q2:
                # q2가 비어있으면 계산 불가능
                break
            q1[i] = abs(q1[i] - q2.pop())

        while q1 and q1[0] == 0:
            # 앞에 0이 존재하면 빼버린다.
            q1.popleft()

    elif c == '*':
        # 곱하기
        if len(q1) < len(q2):
            # q2의 길이가 더 클 경우 q2가 답이므로 q1, q2를 교체한다.
            q1, q2 = q2, q1

        elif len(q1) == len(q2):
            # 길이가 같을 경우, 맨 윗자리부터 체크한다.
            for i in range(len(q1)):
                if q1[i] > q2[i]:
                    break
                elif q1[i] < q2[i]:
                    # q2가 더 크면 q1, q2를 교체한다.
                    q1, q2 = q2, q1
                    break
        while q2:
            # q2를 전부 비운다.
            q2.pop()
    else:
        # 나누기
        use_div = True
        if (i+1) < (len(a) - 1):
            # 나누기는 항상 마지막에 들어가야 한다.
            print("ERROR")
            failed = True
            break

        # 나눌 k값 숫자로 구하기
        k, i, l = 0, -1, len(q1)
        while q2:
            i += 1
            k += q2.pop() * (10 ** i)
        
        if k == 0 or l < k:
            # k가 0이거나 문자열의 길이보다 더 크면 구할 수 없다.
            print("ERROR")
            failed = True
            break

        size, mod, res = math.ceil(l / k), l % k, []
        # size: 짤라야 할 문자열의 길이
        # mod: 문자열의 길이와 k값의 나머지
        # res: 출력해야 할 배열

        for _ in range(mod):
            # mod 갯수 가지 size길이대로 쪼개기
            is_zero = True
            v = ""
            for i in range(size):
                v += str(q1.popleft())
            res.append(int(v))
        
        if mod > 0:
            # mod 이후에는 길이가 모자라므로 size에서 1을 뺀다.
            size -= 1
        
        for _ in range(k - mod):
            v = ""
            for _ in range(size):
                v += str(q1.popleft())
            res.append(int(v))

        for i in range(len(res)):
            v = str(res[i])
            if len(v) > 10:
                print(v[-10:], end=' ')
            else:
                print(v, end=' ')

cnt = 0
if not failed:
    # 계산 성공
    if not q1 and not use_div:
        # q1에 아무것도 없고 나누기를 하지 않았을 경우
        print(0)
    if q1:
        # q1에 데이터가 존재하는 경우
        # 10자리 까지만 출력
        s = ""
        if len(q1) >= 10:
            for i in range(10):
                s = str(q1.pop()) + s
        else:
            while q1:
                s += str(q1.popleft())
        print(s)