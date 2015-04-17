#!/usr/bin/env python3
# -*- coding: utf-8 -*-


EPSILON = 10 ** (-7)


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __xor__(self, other):
        return self.x * other.y - self.y * other.x

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def unit(self):
        return self * (1 / self.norm())


class Point(Vector):
    
    def __repr__(self):
        return Vector.__repr__(self).replace('Vector', 'Point')



class Line:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.a = p1.y - p0.y
        self.b = p0.x - p1.x
        self.c = p0.x * (p0.y - p1.y) + p0.y * (p1.x - p0.x)

    def __rmod__(self, c):
        a = self.p0
        b = self.p1
        ab = b - a
        ac = c - a
        p = ab * ac / ab.norm() * ab.unit() + a
        return p

    def _substitute(self, p):
        return self.a * p.x + self.b * p.y + self.c

    def __contains__(self, p):
        return abs(self._substitute(p)) < EPSILON
    
    def __repr__(self):
        return 'Line({0}, {1})'.format(self.p0, self.p1)



class Ray(Line):
    
    def __contains__(self, p):
        return p in super() and (p - self.p0) * (self.p1 - self.p0) > -EPSILON

    def __repr__(self):
        return repr(super()).replace('Line', 'Ray')
    
    

class Segment(Line):

    def __contains__(self, p):
        return p in Ray(self.p0, self.p1) and p in Ray(self.p1, self.p0)

    def __repr__(self):
        return repr(super()).replace('Line', 'Segment')
    


def read_ints():
    return [int(i) for i in input().split()]


def main():
    # global input
    # global print
    
    # fin = open('input.txt', 'r')
    # input = fin.readline
    # fout = open('output.txt', 'w')
    # _print = print
    # print = lambda *args, **kwargs: _print(*args, file=fout, **kwargs)    
    
    c, a, b = [Point(*read_ints()) for i in range(3)]
    line = Line(a, b)
    ray = Ray(a, b)
    segment = Segment(a, b)
    p = c % line

    print((c - p).norm())

    if p in ray:
        print((c - p).norm())
    else:
        print((c - a).norm())

    if p in segment:
        print((c - p).norm())
    else:
        print(min((c - a).norm(), (c - b).norm()))

    # fout.close()

if __name__ == '__main__':
    main()
