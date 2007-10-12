#!/usr/bin/python

import grammar

class Signal(object):
    def __init__(self, var_type, size, reference):
        self.type = var_type
        self.size = size
        self.reference = reference

    def __str__(self):
        return "Signal(%s, %s, %s)" % (self.type, self.size, self.reference)

class Vcd(object):
    def __init__(self, filename):
        parse_tree = grammar.vcd.parseFile(filename)

        self.signals = {}
        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'signal':
                self.signals[i[2]] = Signal(i[0], i[1], i[3])
