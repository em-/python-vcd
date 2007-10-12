#!/usr/bin/python

import grammar

class Vcd(object):
    def __init__(self, filename):
        parse_tree = grammar.vcd.parseFile(filename)

        self.signals = []
        for i in parse_tree:
            if hasattr(i, 'getName') and i.getName() == 'signal':
                self.signals.append(i)
