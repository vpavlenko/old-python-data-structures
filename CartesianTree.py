#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CartesianTree:
    '''Build an ordered collection of unique elements. An order should be total.
    All the operations run in O(log n) time (average case). However,
    this data structure depends on random number generator, which may cause
    a slowdown to O(n) time on specially developed series of queries.

    >>> ct = CartesianTree([5, 2])
    >>> ct
    [2, 5]
    >>> ct.add(3)
    >>> ct
    [2, 3, 5]
    >>> 3 in ct
    True
    >>> 4 in ct
    False
    >>> len(ct)
    3
    >>> ct.remove(3)
    >>> len(ct)
    2
    >>> ct.add(7)
    >>> len(ct)
    3
    >>> 3 in ct
    False
    >>> 4 in ct
    False
    >>> 5 in ct
    True
    >>> 7 in ct
    True
    >>> ct
    [2, 5, 7]
    >>> ct[0]
    2
    >>> ct[1]
    5
    >>> ct[2]
    7
    >>> ct[3]
    Traceback (most recent call last):
    ...
    IndexError: index out of range
    >>> ct.next(4)
    5
    >>> ct.next(5)
    7
    >>> ct.prev(4)
    2
    >>> ct.prev(2)
    Traceback (most recent call last):
    ...
    ValueError: no such element
    >>> ct.next(7)
    Traceback (most recent call last):
    ...
    ValueError: no such element
    '''

    class __Node:

        '''Store a single value. All the values in the left subtree are less than ours. 
        All the values in the right subtree are greater than ours.
        '''

        import random

        random.seed(43670)

        RANDOMRANGE = 2 ** 16

        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.priority = self.random.randrange(0, self.RANDOMRANGE)
            self.size = 1

        def __recalc(self):
            self.size = self.sizeof(self.left) + 1 + self.sizeof(self.right)

        @classmethod
        def split(cls, node, value):
            '''Return a triple of subtrees (left, center, right). 
            All the values in the left subtree are less than the passed value. 
            The center subtree is None or contains a single node with the passed value.
            All the values in the right subtree are greater or equal than the passed value.
            Don't use the reference 'node' after splitting it: 
            there is no warranty about what should it contain.
            '''
            if node is None:
                return None, None, None
            elif node.value < value:
                left, center, right = cls.split(node.right, value)
                node.right = left
                node.__recalc()
                return node, center, right
            elif node.value == value:
                left, center, right = node.left, node, node.right
                node.left = node.right = None
                node.__recalc()
                return left, center, right
            else:
                left, center, right = cls.split(node.left, value)
                node.left = right
                node.__recalc()
                return left, center, node

        @classmethod
        def merge(cls, *subtrees):
            '''Return a tree. All the value in the given first subtree should be 
            less than the minimal value in the second subtree, and the same 
            relationship should exist between every two subsequent subtrees.
            Don't use the references from 'subtrees' after merging them: 
            there is no warranty about what should they contain.
            '''
            assert len(subtrees) > 0
            if len(subtrees) == 1:
                return subtrees[0]
            elif len(subtrees) > 2:
                return cls.merge(cls.merge(*subtrees[:2]), *subtrees[2:])

            left, right = subtrees
            if left is None:
                return right
            elif right is None:
                return left
            elif left.priority > right.priority:
                left.right = cls.merge(left.right, right)
                left.__recalc()
                return left
            else:
                right.left = cls.merge(left, right.left)
                right.__recalc()
                return right

        @classmethod
        def sizeof(cls, node):
            return node.size if node is not None else 0
            
        def get_kth_node(self, k):
            if k < 0:
                k = self.size + k
            if not (0 <= k < self.size):
                raise IndexError('index out of range')
            left_size = self.sizeof(self.left)
            if left_size == k:
                return self
            elif left_size > k:
                return self.left.get_kth_node(k)
            else:
                return self.right.get_kth_node(k - left_size - 1)

        def __repr__(self):
            return '[{0}] {1} (len={2}) [{3}]'.format(self.left, self.value, self.size, self.right)

    def __init__(self, values):
        self.__root = None
        for value in values:
            self.add(value)

    def add(self, value):
        if value not in self:
            left, center, right = self.__Node.split(self.__root, value)
            self.__root = self.__Node.merge(left, self.__Node(value), right)

    def __contains__(self, value):
        left, center, right = self.__Node.split(self.__root, value)
        retval = center is not None
        self.__root = self.__Node.merge(left, center, right)
        return retval

    def remove(self, value):
        if value not in self:
            raise ValueError()
        left, center, right = self.__Node.split(self.__root, value)
        self.__root = self.__Node.merge(left, right)

    def discard(self, value):
        try:
            self.remove(value)
        except ValueError:
            pass

    def __len__(self):
        return self.__Node.sizeof(self.__root)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError('cartesian tree indices must be integers')
        if self.__root is None:
            raise IndexError('index out of range')
        return self.__root.get_kth_node(index).value

    def next(self, value):
        left, center, right = self.__Node.split(self.__root, value)
        try:
            if self.__Node.sizeof(right) == 0:
                raise ValueError('no such element')
            else:
                retval = right.get_kth_node(0).value
        finally:
            self.__root = self.__Node.merge(left, center, right)
        return retval

    def prev(self, value):
        left, center, right = self.__Node.split(self.__root, value)
        try:
            if self.__Node.sizeof(left) == 0:
                raise ValueError('no such element')
            retval = left.get_kth_node(-1).value
        finally:
            self.__root = self.__Node.merge(left, center, right)
        return retval
    
    def __repr__(self):
        return repr(list(self))


if __name__ == '__main__':
    import doctest
    doctest.testmod()