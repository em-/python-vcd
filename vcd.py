#!/usr/bin/python

import sys
from pyparsing import Word, Group, SkipTo, Literal, Suppress, ZeroOrMore, alphas, nums, alphanums, printables, oneOf

if len(sys.argv) != 2:
    print "Usage: %s FILE" % sys.argv[0]
    sys.exit(2)

signal_id = Word(printables).setResultsName('signal_id')
signal_definition = Word(alphas) + Word(nums) + signal_id + Word(printables)
signal = Group(Suppress('$') + Literal('var') + signal_definition + Suppress('$end'))
section = Group(Suppress('$') + Word(alphas) + SkipTo('$end') + Suppress('$end')).setResultsName('section')

time = Suppress(Literal('#')) + Word(nums).setResultsName('time')

std_logic = oneOf('U X 0 1 Z W L H-').setResultsName('std_logic')
std_logic_vector = Group(Literal('b') + Word('UX01ZWLH-')).setResultsName('std_logic_vector')
value = (Group(std_logic + signal_id) | Group(std_logic_vector + signal_id)).setResultsName('value')

change = Group(time + ZeroOrMore(value)).setResultsName('change')

vcd = (ZeroOrMore(signal | section) + ZeroOrMore(change)).setResultsName('vcd')

print vcd.parseFile(sys.argv[1]).asXML()
