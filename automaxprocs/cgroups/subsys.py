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

    subsys_id = int(fields[_csFieldIDID])
    subsystems = fields[_csFieldIDSubsystems].split(_cgroupSubsysSep)
    name = fields[_csFieldIDName]
    subsys = CGroupSubsys(subsys_id, subsystems, name)
    return subsys


def parse_cgroup_subsystems(proc_path_cgroup: str) -> Dict[str, CGroupSubsys]:
    subsystems = {}
    with open(proc_path_cgroup, mode='r') as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            cgroup = new_cgroup_subsys_from_line(line)
            for subsys in cgroup.Subsystems:
                subsystems[subsys] = cgroup

    return subsystems
