#!/usr/bin/env python3


class TreeRangeQuery:
    '''Build an array of fixed length with fast implementation of range queries. 
    Items of an array should not be None. Operation should be associative.

    >>> rsq = TreeRangeQuery([2, 4, 1, 7, 9], int.__add__)
    >>> rsq
    TreeRangeQuery([2, 4, 1, 7, 9], int.__add__)
    >>> rsq.query(0, 2)
    6
    >>> rsq.query(0, 5)
    23
    >>> rsq[2]
    1
    >>> rsq[2] = 5
    >>> rsq[-2:]
    [7, 9]
    >>> rsq
    TreeRangeQuery([2, 4, 5, 7, 9], int.__add__)
    >>> rsq.query(2, 4)
    12
    >>> rmq = TreeRangeQuery([2, 4, 1, 7, 9], min)
    >>> rmq
    TreeRangeQuery([2, 4, 1, 7, 9], min)
    >>> rmq.query(0, 2)
    2
    >>> rmq.query(0, 5)
    1
    '''

    def __init__(self, iterable, operation):
        self.a = list(iterable)
        self.op = operation

        assert self.a

        self.actual_length = len(self.a)
        self.pow2_length = 1
        while self.pow2_length < self.actual_length:
            self.pow2_length *= 2

        self.a = [None] * (self.pow2_length - 1) + self.a + [None] * (self.pow2_length - self.actual_length)
        for i in range(self.pow2_length - 2, -1, -1):
            if self.a[2 * i + 2] is not None:
                self.a[i] = self.op(self.a[2 * i + 1], self.a[2 * i + 2])
            elif self.a[2 * i + 1] is not None:
                self.a[i] = self.a[2 * i + 1]


    def __repr__(self):
        if '__objclass__' in dir(self.op):
            methodname = self.op.__objclass__.__name__ + '.' + self.op.__name__
        else:
            methodname = self.op.__name__
        return 'TreeRangeQuery({0}, {1})'.format(self.a[self.pow2_length - 1:self.pow2_length - 1 + self.actual_length], methodname)


    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                assert -index <= self.actual_length, 'Index out of bounds'
                return self.a[index]
            else:
                assert index < self.actual_length, 'Index out of bounds'
                return self.a[index + self.pow2_length - 1]
        elif isinstance(index, slice):
            return list.__getitem__(self.a[self.pow2_length - 1:self.pow2_length - 1 + self.actual_length], index)
        else:
            raise TypeError()


    def __setitem__(self, index, value):
        if isinstance(index, int):
            if index < 0:
                assert -index <= self.actual_length, 'Index out of bounds'
                index = self.pow2_length - index
            else:
                assert index < self.actual_length, 'Index out of bounds'
            index += self.pow2_length - 1
            self.a[index] = value
            while index > 0:
                index = (index - 1) // 2
                if self.a[2 * index + 2] is not None:
                    self.a[index] = self.op(self.a[2 * index + 1], self.a[2 * index + 2])                
                else:
                    self.a[index] = self.a[2 * index + 1]
        else:
            raise TypeError()


    def _query_recursion(self, query_left, query_right, index, actual_left, actual_right):
        if query_left <= actual_left and actual_right <= query_right:
            return self.a[index]
        else:
            mid = (actual_left + actual_right) // 2
            if query_right <= mid:
                return self._query_recursion(query_left, query_right, 2 * index + 1, actual_left, mid)
            elif mid <= query_left:
                return self._query_recursion(query_left, query_right, 2 * index + 2, mid, actual_right)
            else:
                return self.op(self._query_recursion(query_left, query_right, 2 * index + 1, actual_left, mid),
                               self._query_recursion(query_left, query_right, 2 * index + 2, mid, actual_right))


    def query(self, query_left, query_right):
        assert query_left < query_right
        return self._query_recursion(query_left, query_right, 0, 0, self.pow2_length)




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

    k = read_ints()[0]
    MAXN = 100001
    rminq = TreeRangeQuery([n ** 2 % 12345 + n ** 3 % 23456 for n in range(0, MAXN)], min)
    rmaxq = TreeRangeQuery([n ** 2 % 12345 + n ** 3 % 23456 for n in range(0, MAXN)], max)

    for i in range(k):
        x, y = read_ints()
        if x > 0:
            print(rmaxq.query(x, y + 1) - rminq.query(x, y + 1))
        else:
            rminq[abs(x)] = y
            rmaxq[abs(x)] = y

    #fout.close()


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    main()