#!/usr/bin/env python3


class SparseTableRangeQuery:
    '''Build an immutable array of fixed length with fast implementation of range queries. 
    Operation should be associative and idempotent (i.e. x == op(x, x)). Examples: min, max.
    The construction of a table runs in O(n log n) time. 
    Each query runs in O(1) time.
    Memory overhead is (n log n).

    >>> rmq = SparseTableRangeQuery([2, 4, 1, 7, 9, 8, 7, 6, 5], min)
    >>> rmq
    SparseTableRangeQuery([2, 4, 1, 7, 9, 8, 7, 6, 5], min)
    >>> rmq.query(0, 2)
    2
    >>> rmq.query(0, 5)
    1
    >>> rmq.query(4, 5)
    9
    >>> rmq.query(4, 6)
    8
    >>> rmq.query(4, 7)
    7
    >>> rmq.query(4, 8)
    6
    >>> rmq.query(4, 9)
    5
    '''

    def __init__(self, iterable, operation):
        a = list(iterable)
        self.op = operation

        assert a

        self.actual_length = len(a)
        self.pow2_length = 1
        num_levels = 0
        while self.pow2_length < self.actual_length:
            self.pow2_length *= 2
            num_levels += 1

        tmp_level = -1
        tmp_leftmost_bit = 0
        self.level = [None]
        self.leftmost_bit = [None]
        for i in range(1, self.actual_length + 1):
            if i & (i - 1) == 0:
                tmp_level += 1
                tmp_leftmost_bit = 2 ** tmp_level
            self.level.append(tmp_level)
            self.leftmost_bit.append(tmp_leftmost_bit)

        self.table = [a]
        pow2 = 1
        for i in range(1, num_levels + 1):
            self.table.append([])
            pow2 *= 2
            j = 0
            while j + pow2 <= self.actual_length:
                self.table[i].append(self.op(self.table[i - 1][j], self.table[i - 1][j + pow2 // 2]))
                j += 1        


    def __repr__(self):
        if '__objclass__' in dir(self.op):
            methodname = self.op.__objclass__.__name__ + '.' + self.op.__name__
        else:
            methodname = self.op.__name__
        return 'SparseTableRangeQuery({0}, {1})'.format(self.table[0], methodname)


    def __getitem__(self, index):
        return self.table[0][index]


    def query(self, query_left, query_right):
        assert query_left < query_right
        diff = query_right - query_left
        level = self.level[diff]
        return self.op(self.table[level][query_left], 
                       self.table[level][query_right - self.leftmost_bit[diff]])




def read_ints():
    return [int(i) for i in input().split()]



def main():
    global input
    global print

    #fin = open('input.txt', 'r')
    #input = fin.readline
    #fout = open('output.txt', 'w')
    #_print = print
    #print = lambda *args, **kwargs: _print(*args, file=fout, **kwargs)

    n, m, a0 = read_ints()
    u, v = read_ints()
    a = [0, a0]
    for i in range(1, n):
        a.append((23 * a[-1] + 21563) % 16714589)

    sparse = SparseTableRangeQuery(a, min)
    for i in range(1, m + 1):
        old_u, old_v = u, v
        ans = sparse.query(min(u, v), max(u, v) + 1)
        u, v = (17 * u + 751 + ans + 2 * i) % n + 1, (13 * v + 593 + ans + 5 * i) % n + 1

    print(old_u, old_v, ans)

    #fout.close()


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    main()