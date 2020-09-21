# -*- coding: utf-8 -*-

import multiprocessing
from .runtime import cpu_quota_to_max_procs


def get_cpu_count():
    return multiprocessing.cpu_count()


def get_max_procs():
    max_procs, status = cpu_quota_to_max_procs(1)
    if status == -1:
        return get_cpu_count()
    return max_procs
