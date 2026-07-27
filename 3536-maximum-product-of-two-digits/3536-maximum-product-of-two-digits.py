class Solution(object):
    def maxProduct(self, n):
        """
        :type n: int
        :rtype: int
        """
        max1 = -1
        max2 = -1

        while n > 0:
            digit = n % 10

            if digit > max1:
                max2 = max1
                max1 = digit
            elif digit > max2:
                max2 = digit

            n //= 10

        return max1 * max2