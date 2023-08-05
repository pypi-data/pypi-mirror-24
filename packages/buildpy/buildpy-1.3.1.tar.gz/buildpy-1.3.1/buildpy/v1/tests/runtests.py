#!/usr/bin/python

import sys

import buildpy.v1


def main(argv):
    def let():
        s = buildpy.v1._TSet()
        s.add(s.add(s.add(1)))
        assert len(s) == 2
        s.remove(s.remove(1))
        assert len(s) == 0
    let()


if __name__ == '__main__':
    main(sys.argv)
