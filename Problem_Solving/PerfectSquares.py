import math


def perfectSq(n):
    dp = [0] * (n + 1)
    for i in range(n + 1):
        if dp[i] == 0:
            dp[i] = i
        if i * i <= n:
            dp[i * i] = 1

    # after initializing dp array fill dp array

    for i in range(1, n + 1):
        for j in range(1,i):
            if i + j * j <= n:
                dp[i + j * j] = min(dp[i + j * j], dp[i] + 1)
    print(dp)


perfectSq(30)