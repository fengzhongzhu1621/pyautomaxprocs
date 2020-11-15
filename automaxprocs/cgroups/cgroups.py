# -*- coding: utf-8 -*-

from collections import UserDict
from typing import Dict
from .subsys import parse_cgroup_subsystems
from .mountpoint import MountPoint, parse_mount_info
from .errors import (
    CgroupSubsysFormatInvalidError,
    MountPointFormatInvalidError,
    PathNotExposedFromMountPointError)
from .cgroup import CGroup


# _cgroupFSType is the Linux CGroup file system type used in
# `/proc/$PID/mountinfo`.
_cgroupFSType = "cgroup"
# _cgroupSubsysCPU is the CPU CGroup subsystem.
_cgroupSubsysCPU = "cpu"
# _cgroupSubsysCPUAcct is the CPU accounting CGroup subsystem.
_cgroupSubsysCPUAcct = "cpuacct"
# _cgroupSubsysCPUSet is the CPUSet CGroup subsystem.
_cgroupSubsysCPUSet = "cpuset"
# _cgroupSubsysMemory is the Memory CGroup subsystem.
_cgroupSubsysMemory = "memory"

# cfs 是完全公平调度器的缩写，即按照比例进行cpu分配调度
# cpu.cfs_period_us和cpu.cfs_quota_us来限制该组中的所有进程在单位时间里可以使用的cpu时间
# 例如：周期为1秒，假设CPU>=4核心，表示这个组在一个使用周期(1s)内可以跑满4核资源
# cpu.cfs_period_us = 1000000
# cpu.cfs_quota_us = 4000000
# _cgroupCPUCFSQuotaUsParam is the file name for the CGroup CFS quota
# parameter.
# 设置cpu.cfs_period_us周期内cgroup可使用的cpu
# 默认 -1，表示使用的CPU不受cgroup限制；最小值为1ms(1000)，最大值为1s
_cgroupCPUCFSQuotaUsParam = "cpu.cfs_quota_us"
# _cgroupCPUCFSPeriodUsParam is the file name for the CGroup CFS period
# parameter.
# 周期内允许占用的CPU时间，默认为 100000，单位为微秒us
_cgroupCPUCFSPeriodUsParam = "cpu.cfs_period_us"

# /proc/self 下是当前进程的信息
# /proc/self/cgroup 是当前进程的cgroup信息
_procPathCGroup = "/proc/self/cgroup"
# 记录当前系统所有挂载文件系统的信息
_procPathMountInfo = "/proc/self/mountinfo"


class CGroups(UserDict):
    def cpu_quota(self):
        cpu_cgroup = self.get(_cgroupSubsysCPU)
        if not cpu_cgroup:
            return -1, False

        try:
            cfs_quota_us = cpu_cgroup.read_int(_cgroupCPUCFSQuotaUsParam)
        except ValueError:
            return -1, False
        if cfs_quota_us <= 0:
            return -1, False

        try:
            cfs_period_us = cpu_cgroup.read_int(_cgroupCPUCFSPeriodUsParam)
        except ValueError:
            return -1, False

        if cfs_period_us == 0:
            return -1, False

        quota = float(cfs_quota_us) / float(cfs_period_us)
        return quota, True


def new_cgroups(proc_path_mount_info,
                proc_path_cgroup: str) -> Dict[str, CGroups]:
    """

    :param proc_path_mount_info: 当前系统所有挂载文件系统的信息
    :param proc_path_cgroup: 当前进程的cgroup信息
    :return:
    """
    # 解析当前进程的cgroup子系统信息
    try:
        cgroup_subsystems = parse_cgroup_subsystems(proc_path_cgroup)
    except (ValueError, CgroupSubsysFormatInvalidError):
        return
    cgroups = {}

    def new_mount_point(mp: MountPoint) -> None:
        # 判断文件系统是否是cgroup
        if mp.fs_type != _cgroupFSType:
            return
        # 遍历超级快选项
        for opt in mp.super_options:
            # 判断cgroups子系统是否存在
            subsys = cgroup_subsystems.get(opt)
            if not subsys:
                continue
            # 获得cgroup的挂载点路径
            cgroup_path = mp.translate(subsys.name)
            cgroups[opt] = CGroup(cgroup_path)

    # 解析挂载的文件系统信息
    try:
        parse_mount_info(proc_path_mount_info, new_mount_point)
    except (FileNotFoundError, MountPointFormatInvalidError, PathNotExposedFromMountPointError):
        return
    return CGroups(cgroups)


def new_cgroups_for_current_process():
    return new_cgroups(_procPathMountInfo, _procPathCGroup)
