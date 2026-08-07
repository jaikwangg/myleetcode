class Solution:
    def smallestNumber(self, num, t):
        """
        :type num: str
        :type t: int
        :rtype: str
        """
        a0 = b0 = c0 = d0 = 0
        tt = t
        while tt % 2 == 0:
            a0 += 1; tt //= 2
        while tt % 3 == 0:
            b0 += 1; tt //= 3
        while tt % 5 == 0:
            c0 += 1; tt //= 5
        while tt % 7 == 0:
            d0 += 1; tt //= 7
        if tt != 1:
            return "-1"   # t มีตัวประกอบเฉพาะอื่นนอกจาก 2,3,5,7 -> เป็นไปไม่ได้

        digit_exp = {
            1: (0,0,0,0), 2: (1,0,0,0), 3: (0,1,0,0), 4: (2,0,0,0),
            5: (0,0,1,0), 6: (1,1,0,0), 7: (0,0,0,1), 8: (3,0,0,0), 9: (0,2,0,0)
        }

        A, B, C, D = a0+1, b0+1, c0+1, d0+1
        # dp[a][b][c][d] = จำนวนหลัก (2..9) น้อยที่สุดที่ใช้ปิด deficit (a,b,c,d)
        dp = [[[[0]*D for _ in range(C)] for _ in range(B)] for _ in range(A)]
        for a in range(A):
            for b in range(B):
                for c in range(C):
                    for d in range(D):
                        if a == 0 and b == 0 and c == 0 and d == 0:
                            continue
                        best = None
                        for x in range(2, 10):
                            e2, e3, e5, e7 = digit_exp[x]
                            na = a-e2 if a > e2 else 0
                            nb = b-e3 if b > e3 else 0
                            nc = c-e5 if c > e5 else 0
                            nd = d-e7 if d > e7 else 0
                            if (na, nb, nc, nd) == (a, b, c, d):
                                continue   # ไม่มีความคืบหน้า -> ห้ามใช้
                            val = 1 + dp[na][nb][nc][nd]
                            if best is None or val < best:
                                best = val
                        dp[a][b][c][d] = best

        def get_dp(a, b, c, d):
            return dp[a][b][c][d]

        def deficit_of(pe2, pe3, pe5, pe7):
            a = a0-pe2 if a0 > pe2 else 0
            b = b0-pe3 if b0 > pe3 else 0
            c = c0-pe5 if c0 > pe5 else 0
            d = d0-pe7 if d0 > pe7 else 0
            return (a, b, c, d)

        def fill_suffix(deficit, slots):
            a, b, c, d = deficit
            res = []
            remaining = slots
            for _ in range(slots):
                remaining -= 1
                for x in range(1, 10):
                    e2, e3, e5, e7 = digit_exp[x]
                    na = a-e2 if a > e2 else 0
                    nb = b-e3 if b > e3 else 0
                    nc = c-e5 if c > e5 else 0
                    nd = d-e7 if d > e7 else 0
                    if get_dp(na, nb, nc, nd) <= remaining:
                        res.append(str(x))
                        a, b, c, d = na, nb, nc, nd
                        break
            return ''.join(res)

        n = len(num)
        firstZero = n
        for idx, ch in enumerate(num):
            if ch == '0':
                firstZero = idx
                break

        # 1) ตรวจ num เอง
        if firstZero == n:
            pe2 = pe3 = pe5 = pe7 = 0
            for ch in num:
                e2, e3, e5, e7 = digit_exp[int(ch)]
                pe2 += e2; pe3 += e3; pe5 += e5; pe7 += e7
            if deficit_of(pe2, pe3, pe5, pe7) == (0, 0, 0, 0):
                return num

        # 2) แก้แบบความยาวเท่าเดิม
        limit = firstZero
        PE2 = [0]*(limit+1); PE3 = [0]*(limit+1)
        PE5 = [0]*(limit+1); PE7 = [0]*(limit+1)
        for i in range(limit):
            e2, e3, e5, e7 = digit_exp[int(num[i])]
            PE2[i+1] = PE2[i]+e2; PE3[i+1] = PE3[i]+e3
            PE5[i+1] = PE5[i]+e5; PE7[i+1] = PE7[i]+e7

        upper = firstZero if firstZero < n else n-1
        answer = None
        for i in range(upper, -1, -1):   # ลองจากตำแหน่งขวาสุดก่อน
            deficit_prefix = deficit_of(PE2[i], PE3[i], PE5[i], PE7[i])
            remaining_slots = n-1-i
            cur_digit = int(num[i])
            for v in range(cur_digit+1, 10):
                e2, e3, e5, e7 = digit_exp[v]
                a, b, c, d = deficit_prefix
                na = a-e2 if a > e2 else 0
                nb = b-e3 if b > e3 else 0
                nc = c-e5 if c > e5 else 0
                nd = d-e7 if d > e7 else 0
                if get_dp(na, nb, nc, nd) <= remaining_slots:
                    answer = num[:i] + str(v) + fill_suffix((na, nb, nc, nd), remaining_slots)
                    break
            if answer is not None:
                break
        if answer is not None:
            return answer

        # 3) ถ้าความยาวเท่าเดิมไม่ได้ ต้องเพิ่มความยาว
        minDigits = get_dp(a0, b0, c0, d0)
        L = max(n+1, minDigits)
        return fill_suffix((a0, b0, c0, d0), L)