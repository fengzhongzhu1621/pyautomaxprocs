# -*- coding: utf-8 -*-

from .runtime import (CPUQuotaStatus, CPUQuotaUndefined)


def cpu_quota_to_max_procs(_: int) -> (int, CPUQuotaStatus):
    return -1, CPUQuotaUndefined
