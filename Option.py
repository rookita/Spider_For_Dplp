# coding: utf-8
import argparse

class BaseOptions():
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._initialized = False
    def initialize(self):
        self._parser.add_argument('-a','--author_name', default="qi chu",type=str, help='the author name')
        self._parser.add_argument('-s','--school', type=str, default="University of Science and Technology of China", help='the work-place of the  author')
        self._parser.add_argument('-d','--department', type=str, default='Electronic Engineering', help='the department of the author')
        self._parser.add_argument('-c','--city', type=str, default='hefei', help='the work city of the author')
        self._parser.add_argument('-C','--country', type=str, default='china', help='the country of the author')
        self._initialized = True

    def parse(self):
        if not self._initialized:
            self.initialize()
        self._opt = self._parser.parse_args()
        return self._opt