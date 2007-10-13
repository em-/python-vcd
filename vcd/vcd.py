#!/usr/bin/python

import grammar

class Signal(object):
    def __init__(self, var_type, size, reference, module):
        self.type = var_type
        self.size = size
        self.reference = reference
        self.module = module
        self.steps = []

    def step(self, time, value):
        self.steps.append((time, value))

    def __str__(self):
        return "Signal(%s, %s, %s, %s)" % (self.type, self.size, self.reference, self.module)

class Vcd(object):
    def __init__(self, filename):
        parse_tree = grammar.vcd.parseFile(filename)

        self.signals = {}
        scope = []
        for i in parse_tree:
            if not hasattr(i, 'getName'): continue
            if i.getName() == 'scope':
                scope.append(i.module)
            if i.getName() == 'upscope':
                scope.pop()
            if i.getName() == 'signal':
                if scope:
                    current_scope = scope[-1]
                else:
                    current_scope = None
                self.signals[i.id] = Signal(i.type, int(i.size), i.name, current_scope)

        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'step':
                time = i.time
                for j in i:
                    if hasattr(j, 'getName') and j.getName() == 'value':
                        self.signals[j.id].step(time, j[0])
