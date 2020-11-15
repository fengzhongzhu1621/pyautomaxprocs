# -*- coding: utf-8 -*-

import os


class CGroup:
    def __init__(self, path):
        self.path = path

    def path(self):
        return self.path

    def param_path(self, param):
        return os.path.join(self.path, param)

    def read_first_line(self, param):
        file_path = self.param_path(param)
        with open(file_path, "r") as reader:
            for row in reader:
                if row:
                    return row.strip()

    def read_int(self, param):
        try:
            first_row = self.read_first_line(param)
        except FileNotFoundError:
            return 0
        try:
            return int(first_row) if first_row else 0
        except ValueError:
            return 0
