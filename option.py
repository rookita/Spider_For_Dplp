# coding: utf-8
import argparse

class BaseOptions():
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._initialized = False
    def initialize(self):
        self._parser.add_argument('-A','--author_name', default="qi chu",type=str, help='the author name')
        self._parser.add_argument('-S','--school', type=str, default="University of Science and Technology of China", help='the work-place of the  author')
        self._parser.add_argument('-D','--department', type=str, default='Electronic Engineering', help='the department of the author')
        self._parser.add_argument('-CT','--city', type=str, default='hefei', help='the work city of the author')
        self._parser.add_argument('-C','--country', type=str, default='china', help='the country of the author')
        self._parser.add_argument('-PCF','--print_cmp_info', default=False,action='store_true',help='print the compare info')
        self._initialized = True

    def parse(self):
        if not self._initialized:
            self.initialize()
        self._opt = self._parser.parse_args()
        return self._opt