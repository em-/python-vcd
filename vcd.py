#!/usr/bin/python

import sys
from pyparsing import (Word, Group, SkipTo,
                       Suppress, ZeroOrMore,
                       alphas, nums, printables,
                       oneOf)

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

type = Word(alphas).setResultsName('type')
size = Word(nums).setResultsName('size')
id = Word(printables).setResultsName('id')
name = Word(printables).setResultsName('name')

signal_definition = type + size + id + name
signal = (Group(Suppress('$') + Suppress('var') + signal_definition + Suppress('$end'))).setResultsName('signal')

content = SkipTo('$end').setResultsName('content') + Suppress('$end')
section_name = Word(alphas).setResultsName('name')
section = Group(Suppress('$') + section_name + content).setResultsName('section')

time = Suppress('#') + Word(nums).setResultsName('time')

std_logic = oneOf('U X 0 1 Z W L H-').setResultsName('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-').setResultsName('std_logic_vector')
value = (Group(std_logic + id) | Group(std_logic_vector + id)).setResultsName('value')

change = Group(time + ZeroOrMore(value)).setResultsName('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change)).setResultsName('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
