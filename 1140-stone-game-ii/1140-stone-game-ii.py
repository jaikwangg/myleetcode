class Solution(object):
    def stoneGameII(self, piles):
        """
        :type piles: List[int]
        :rtype: int
        """
        n = len(piles)
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]

        memo = {}

        def best(i, m):
            if i + 2 * m >= n:
                return suffix[i]
            key = (i, m)
            if key in memo:
                return memo[key]
            res = 0
            for x in range(1, 2 * m + 1):
                res = max(res, suffix[i] - best(i + x, max(m, x)))
            memo[key] = res
            return res

        return best(0, 1)