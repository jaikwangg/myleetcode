import bisect

class Solution(object):
    def validSequence(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: List[int]
        """
        n, m = len(word1), len(word2)

        pos_list = {}
        for i, ch in enumerate(word1):
            pos_list.setdefault(ch, []).append(i)

        def next_at_or_after(c, X):
            lst = pos_list.get(c)
            if not lst:
                return None
            idx = bisect.bisect_left(lst, X)
            return lst[idx] if idx < len(lst) else None

        def last_before(c, X):
            # largest position < X with word1[position] == c, else -1
            if X <= 0:
                return -1
            lst = pos_list.get(c)
            if not lst:
                return -1
            idx = bisect.bisect_left(lst, X)
            return lst[idx-1] if idx > 0 else -1

        # exact[j] = rightmost start i such that word2[j:] embeds EXACTLY
        # as a subsequence of word1[i:]
        exact = [0]*(m+1)
        exact[m] = n
        for j in range(m-1, -1, -1):
            exact[j] = -1 if exact[j+1] < 0 else last_before(word2[j], exact[j+1])

        # allowOne[j] = rightmost start i such that word2[j:] embeds in
        # word1[i:] using AT MOST ONE substitution somewhere in word2[j:]
        allowOne = [0]*(m+1)
        allowOne[m] = n
        for j in range(m-1, -1, -1):
            branch1 = last_before(word2[j], allowOne[j+1]) if allowOne[j+1] >= 0 else -1
            branch2 = (exact[j+1]-1) if exact[j+1] >= 1 else -1
            allowOne[j] = max(branch1, branch2)

        # forward greedy construction
        pos = 0
        changed = False
        result = []
        for j in range(m):
            if not changed:
                idxA = next_at_or_after(word2[j], pos)
                cand_exact = idxA if (idxA is not None and idxA+1 <= allowOne[j+1]) else None
                cand_sub = pos if (pos <= n-1 and pos+1 <= exact[j+1]) else None

                if cand_exact is not None and cand_sub is not None:
                    if cand_exact <= cand_sub:      # only true when idxA == pos
                        result.append(cand_exact); pos = cand_exact+1
                    else:
                        result.append(cand_sub); pos = cand_sub+1; changed = True
                elif cand_exact is not None:
                    result.append(cand_exact); pos = cand_exact+1
                elif cand_sub is not None:
                    result.append(cand_sub); pos = cand_sub+1; changed = True
                else:
                    return []
            else:
                idxA = next_at_or_after(word2[j], pos)
                if idxA is None or idxA+1 > exact[j+1]:
                    return []
                result.append(idxA); pos = idxA+1

        return result