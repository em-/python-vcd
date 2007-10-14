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

        self.signals = []
        id_to_signal = {}
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
                self.signals.append(Signal(i.type, int(i.size), i.name, current_scope))
                id_to_signal[i.id] = self.signals[-1]

        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'step':
                time = i.time
                for j in i:
                    if hasattr(j, 'getName') and j.getName() == 'value':
                        id_to_signal[j.id].step(time, j[0])
