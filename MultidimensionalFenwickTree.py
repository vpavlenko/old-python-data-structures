#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_ints():
    return [int(i) for i in input().split()]


class MultidimensionalFenwickSumTree:
    '''Build a multidimensional table of elements (usually numbers), providing
    item assignment and multidimensional range sum queries.

    Time complexity of operations:
      assume n is maximal index among all dimensions,
             d is number of dimensions.
      * construction: O(n^d log^d n)
      * update: O(log^d n)
      * range sum query: O(2^d log^d n)

    >>> mfst = MultidimensionalFenwickSumTree([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 0, 1]])
    >>> mfst
    MultidimensionalFenwickSumTree([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 0, 1]])
    >>> mfst[0:2][1:3].sum()
    14
    >>> mfst[2][2]
    0
    >>> mfst[2][2] = 8
    >>> mfst
    MultidimensionalFenwickSumTree([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 8, 1]])
    >>> mfst[1:3][0:3].sum()
    40
    '''

    import copy

    class SliceView:
        '''Provide access to elements and subtables of a Fenwick tree.
        self.indices is maintained as a tuple of slice object with step == None
        and 0 <= indices[i].start < self.mfst.length[i],
            indices[i].start < indices[i].stop <= self.mfst.length[i].
        '''

        def __init__(self, mfst, indices):
            self.mfst = mfst
            self.indices = indices

        def __fenwick_rec_update(self, indices, difference, level, subtable):
            k = indices[level].start
            while k < self.mfst.length[level]:
                if level + 1 == self.mfst.dim:
                    subtable[k] += difference
                else:
                    self.__fenwick_rec_update(indices, difference, level + 1, subtable[k])
                k = k | (k + 1)

        def __getitem__(self, index, value=None):
            level = len(self.indices)
            assert level < self.mfst.dim, 'too many levels of indices'

            if isinstance(index, int):
                if index < 0:
                    index += self.mfst.length[level]
                index = slice(index, index + 1)

            if (not 0 <= index.start < self.mfst.length[level] or 
                not index.start < index.stop <= self.mfst.length[level]):
                raise IndexError('index out of range')

            indices = self.indices + (index,)

            if (level + 1 == self.mfst.dim and
                all([i.start + 1 == i.stop for i in indices])):
                tmp = self.mfst.table
                for i in indices[:-1]:
                    tmp = tmp[i.start]
                if value is None:
                    return tmp[indices[-1].start]
                else:
                    difference = value - tmp[indices[-1].start]
                    tmp[indices[-1].start] = value

                    self.__fenwick_rec_update(indices, difference, 0, self.mfst.sum)
            else:
                if value is None:
                    return type(self)(self.mfst, indices)
                else:
                    if level + 1 == self.mfst.dim:
                        raise IndexError('cannot assign to a slice')
                    else:
                        raise IndexError('not enough levels of indices')

        def __setitem__(self, index, value):
            self.__getitem__(index, value)

        def __rec_prefix_sum(self, res, indices, level, subtable):
            k = indices[level] - 1
            while k >= 0:
                if level + 1 == self.mfst.dim:
                    res[0] += subtable[k]
                else:
                    self.__rec_prefix_sum(res, indices, level + 1, subtable[k])
                k = (k & (k + 1)) - 1

        def prefix_sum(self, indices):
            res = [self.mfst.scalar_type()]
            self.__rec_prefix_sum(res, indices, 0, self.mfst.sum)
            return res[0]

        def __rec_sum(self, res, indices, parity, level):
            if level == self.mfst.dim:
                res[0] += parity * self.prefix_sum(indices)
            else:
                indices.append(self.indices[level].start)
                self.__rec_sum(res, indices, -parity, level + 1)
                indices.pop()
                indices.append(self.indices[level].stop)
                self.__rec_sum(res, indices, parity, level + 1)
                indices.pop()

        def sum(self):
            res = [self.mfst.scalar_type()]
            self.__rec_sum(res, [], 1, 0)
            return res[0]

    def __init__(self, table):
        '''Build a table. Parameter 'table' should consist of nested lists. 
        Everything which is not a list inside 'tables' is treated as a scalar 
        value.
        '''
        table = self.copy.deepcopy(table)
        self.length = []
        mainstream_subtable = table
        stack_for_length_check = [mainstream_subtable]

        while isinstance(mainstream_subtable, list):
            self.length.append(len(mainstream_subtable))
            for subtable in stack_for_length_check:
                if len(subtable) != self.length[-1]:
                    raise ValueError('length mismatch on level {0}: '
                        'the subtable {1} should be of length {2} '
                        'as the subtable {3} is'.format(level, subtable,
                            self.length[-1], mainstream_subtable))
            mainstream_subtable = mainstream_subtable[0]
            stack_for_length_check = [j for i in stack_for_length_check 
                                        for j in i]

        self.scalar_type = type(mainstream_subtable)
        self.dim = len(self.length)

        assert self.dim > 0
        assert 0 not in self.length

        self.sum = [self.scalar_type() for i in range(self.length[-1])]
        for i in self.length[-2::-1]:
            self.sum = [self.copy.deepcopy(self.sum) for j in range(i)]

        self.table = self.copy.deepcopy(self.sum)

        def recursive_construction(level, slice_indices, subtable):
            if level < self.dim:
                for i in range(self.length[level]):
                    slice_indices.append(slice(i, i + 1))
                    recursive_construction(level + 1, slice_indices, subtable[i])
                    slice_indices.pop()
            else:
                self.SliceView(self, tuple(slice_indices[:-1]))[slice_indices[-1]] = subtable

        recursive_construction(0, [], table)

    def __repr__(self):
        return 'MultidimensionalFenwickSumTree({0})'.format(repr(self.table))

    def __getitem__(self, index):
        return self.SliceView(self, ())[index]

    def __setitem__(self, index, value):
        self.SliceView(self, ())[index] = value



def main():
    global input
    global print
    
    #fin = open('input.txt', 'r')
    #input = fin.readline
    #fout = open('output.txt', 'w')
    #_print = print
    #print = lambda *args, **kwargs: _print(*args, file=fout, **kwargs)

    n = read_ints()[0]
    mfst = MultidimensionalFenwickSumTree([[[0] * n for i in range(n)] 
                                                    for j in range(n)])
    while True:
        line = read_ints()
        if line[0] == 1:
            x, y, z, k = line[1:]
            mfst[x][y][z] += k
        elif line[0] == 2:
            x1, y1, z1, x2, y2, z2 = line[1:]
            print(mfst[x1:x2 + 1][y1:y2 + 1][z1:z2 + 1].sum())
        else:
            assert line[0] == 3
            break


    #fout.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # main()
