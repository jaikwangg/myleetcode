class Solution(object):
    def findRotation(self, mat, target):
        """
        :type mat: List[List[int]]
        :type target: List[List[int]]
        :rtype: bool
        """
        n = len(mat)
        # Track validity of 0 deg, 90 deg, 180 deg, and 270 deg rotations
        r0 = r90 = r180 = r270 = True

        for r in range(n):
            for c in range(n):
                if mat[r][c] != target[r][c]:
                    r0 = False
                if mat[n - 1 - c][r] != target[r][c]:
                    r90 = False
                if mat[n - 1 - r][n - 1 - c] != target[r][c]:
                    r180 = False
                if mat[c][n - 1 - r] != target[r][c]:
                    r270 = False

        return r0 or r90 or r180 or r270
        