# -*- coding: utf-8 -*-

import platform
import math
from .runtime import (
    CPUQuotaStatus,
    CPUQuotaUndefined,
    CPUQuotaMinUsed,
    CPUQuotaUsed)
from ..cgroups.cgroups import new_cgroups_for_current_process


def cpu_quota_to_max_procs(min_value: int) -> (int, CPUQuotaStatus):
    # 当前进程的cgroup信息
    cgroups = new_cgroups_for_current_process()
    if not cgroups:
        return -1, CPUQuotaUndefined

    quota, defined = cgroups.cpu_quota()
    if not defined:
        return -1, CPUQuotaUndefined

    max_procs = int(math.floor(quota))

    if min_value > 0 and max_procs < min_value:
        return min_value, CPUQuotaMinUsed

    return max_procs, CPUQuotaUsed
