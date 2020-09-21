# -*- coding: utf-8 -*-

import os


class CGroup:
    def __init__(self, path):
        self.path = path

    def path(self):
        return self.path

    def param_path(self, param):
        return os.path.join(self.path, param)

    def rea_first_line(self, param):
        file_path = self.param_path(param)
        with open(file_path, "r") as reader:
            for row in reader:
                if row:
                    return row.strip()

    def read_int(self, param):
        first_row = self.rea_first_line(param)
        return int(first_row)
