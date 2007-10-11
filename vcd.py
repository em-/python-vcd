#!/usr/bin/python

import sys
from pyparsing import Word, Group, SkipTo, Suppress, ZeroOrMore, alphas

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

section = Group(Suppress('$') + Word(alphas) + SkipTo('$end') + Suppress('$end'))

vcd = ZeroOrMore(section)

print vcd.parseFile(sys.argv[1]).asXML()
