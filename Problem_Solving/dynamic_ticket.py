from functools import lru_cache


def mincostTickets(days, costs):
    dayset = set(days)
    durations = [1, 7, 30]

    def dp(i):
        if i > 365:
            return 0
        elif i in dayset:
            return min(dp(i + d) + c
                       for c, d in zip(costs, durations))
        else:
            return dp(i + 1)

    return dp(1)

days = [1,4,6,7,8]
costs = [2,7,15]

mincostTickets(days, costs)
print('done')
