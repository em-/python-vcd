#!/usr/bin/python

import sys
from pyparsing import Word, Group, SkipTo, Literal, Suppress, ZeroOrMore, alphas, nums, printables

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

signal_definition = Word(alphas) + Word(nums) + Word(printables) + Word(printables)
signal = Group(Suppress('$') + Literal('var') + signal_definition + Suppress('$end'))
section = Group(Suppress('$') + Word(alphas) + SkipTo('$end') + Suppress('$end'))

vcd = ZeroOrMore(signal | section)

print vcd.parseFile(sys.argv[1]).asXML()
