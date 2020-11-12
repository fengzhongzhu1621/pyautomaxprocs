# -*- coding: utf-8 -*-

from typing import List, Dict
from .errors import CgroupSubsysFormatInvalidError


_cgroupSep = ":"
_cgroupSubsysSep = ","

_csFieldIDID = 0
_csFieldIDSubsystems = 1
_csFieldIDName = 2
_csFieldCount = 3


class CGroupSubsys:
    def __init(self, subsys_id: int, subsystems: List[str], name: str):
        self.id = subsys_id
        self.subsystems = subsystems
        self.name = name


def new_cgroup_subsys_from_line(line: str) -> CGroupSubsys:
    fields = line.split(_cgroupSep)
    if len(fields) != _csFieldCount:
        raise CgroupSubsysFormatInvalidError(line)

    # 第0列是子系统ID
    subsys_id = int(fields[_csFieldIDID])
    # 可能有多个子系统
    subsystems = fields[_csFieldIDSubsystems].split(_cgroupSubsysSep)
    # 子系统路径
    name = fields[_csFieldIDName]
    subsys = CGroupSubsys(subsys_id, subsystems, name)
    return subsys


def parse_cgroup_subsystems(proc_path_cgroup: str) -> Dict[str, CGroupSubsys]:
    """解析当前进程的cgroup子系统信息 ."""
    subsystems = {}
    with open(proc_path_cgroup, mode='r') as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            cgroup = new_cgroup_subsys_from_line(line)
            for subsys in cgroup.subsystems:
                subsystems[subsys] = cgroup

    return subsystems
