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

type = Word(alphas).setResultsName('type')
size = Word(nums).setResultsName('size')
id = Word(printables).setResultsName('id')
name = Word(printables).setResultsName('name')

signal_definition = type + size + id + name
signal = (g(s('$var') + signal_definition + s('$end'))).setResultsName('signal')

content = SkipTo('$end').setResultsName('content') + s('$end')
section_name = Word(alphas).setResultsName('name')
section = g(s('$') + section_name + content).setResultsName('section')

time = s('#') + Word(nums).setResultsName('time')

std_logic = oneOf('U X 0 1 Z W L H-').setResultsName('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-').setResultsName('std_logic_vector')
value = (g(std_logic + id) | g(std_logic_vector + id)).setResultsName('value')

change = g(time + ZeroOrMore(value)).setResultsName('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change)).setResultsName('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
