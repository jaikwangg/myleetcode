import math

class Solution(object):
    def minNumberOfSeconds(self, mountainHeight, workerTimes):
        """
        :type mountainHeight: int
        :type workerTimes: List[int]
        :rtype: int
        """
        def max_units(t, seconds):
            # largest k with t*k*(k+1)//2 <= seconds
            work = seconds // t
            k = int((math.sqrt(8.0 * work + 1) - 1) // 2)
            while k * (k + 1) // 2 > work:
                k -= 1
            while (k + 1) * (k + 2) // 2 <= work:
                k += 1
            return k

        def can_finish(seconds):
            total = 0
            for t in workerTimes:
                total += max_units(t, seconds)
                if total >= mountainHeight:
                    return True
            return False

        lo, hi = 1, max(workerTimes) * mountainHeight * (mountainHeight + 1) // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if can_finish(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo