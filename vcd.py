#!/usr/bin/python

import sys
from pyparsing import (Word, Group, SkipTo,
                       Suppress, ZeroOrMore,
                       alphas, nums, printables,
                       oneOf)

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

s = Suppress

type = Word(alphas)('type')
size = Word(nums)('size')
id   = Word(printables)('id')
name = Word(printables)('name')

definition = type + size + id + name
signal     = Group(s('$var') + definition + s('$end'))('signal')

content      = SkipTo('$end')('content') + s('$end')
section_name = Word(alphas)('name')
section      = Group(s('$') + section_name + content)('section')

time = s('#') + Word(nums)('time')

std_logic        = oneOf('U X 0 1 Z W L H-')('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-')('std_logic_vector')

value  = (Group(std_logic + id) | Group(std_logic_vector + id))('value')
change = Group(time + ZeroOrMore(value))('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change))('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
