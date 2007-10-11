#!/usr/bin/python

import sys
from pyparsing import (Word, Group, SkipTo, Literal,
                       Suppress, ZeroOrMore,
                       alphas, nums, printables,
                       oneOf)

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

signal_id = Word(printables).setResultsName('identifier')

type = Word(alphas).setResultsName('type')
size = Word(nums).setResultsName('size')
name = Word(printables).setResultsName('name')

signal_definition = type + size + signal_id + name
signal = (Group(Suppress('$') + Suppress(Literal('var')) + signal_definition + Suppress('$end'))).setResultsName('signal')

content = SkipTo('$end').setResultsName('content') + Suppress('$end')
section_name = Word(alphas).setResultsName('name')
section = Group(Suppress('$') + section_name + content).setResultsName('section')

time = Suppress(Literal('#')) + Word(nums).setResultsName('time')

std_logic = oneOf('U X 0 1 Z W L H-').setResultsName('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-').setResultsName('std_logic_vector')
value = (Group(std_logic + signal_id) | Group(std_logic_vector + signal_id)).setResultsName('value')

change = Group(time + ZeroOrMore(value)).setResultsName('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change)).setResultsName('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
