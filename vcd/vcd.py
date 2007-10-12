#!/usr/bin/python

import grammar

class Signal(object):
    def __init__(self, var_type, size, reference):
        self.type = var_type
        self.size = size
        self.reference = reference
        self.steps = []

    def step(self, time, value):
        self.steps.append((time, value))

    def __str__(self):
        return "Signal(%s, %s, %s)" % (self.type, self.size, self.reference)

class Vcd(object):
    def __init__(self, filename):
        parse_tree = grammar.vcd.parseFile(filename)

        self.signals = {}
        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'signal':
                self.signals[i.id] = Signal(i.type, i.size, i.name)

        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'step':
                time = i.time
                for j in i:
                    if hasattr(j, 'getName') and j.getName() == 'value':
                        self.signals[j.id].step(time, j[0])
