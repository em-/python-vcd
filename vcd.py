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
g = Group

type = Word(alphas)('type')
size = Word(nums)('size')
id = Word(printables)('id')
name = Word(printables)('name')

definition = type + size + id + name
signal = g(s('$var') + definition + s('$end'))('signal')

content = SkipTo('$end')('content') + s('$end')
section_name = Word(alphas)('name')
section = g(s('$') + section_name + content)('section')

time = s('#') + Word(nums)('time')

std_logic = oneOf('U X 0 1 Z W L H-')('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-')('std_logic_vector')
value = g(std_logic + id) | g(std_logic_vector + id)('value')

change = g(time + ZeroOrMore(value))('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change))('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
