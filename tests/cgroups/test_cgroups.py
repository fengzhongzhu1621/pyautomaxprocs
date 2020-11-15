# -*- coding: utf-8 -*-

import os

import pytest
from automaxprocs.cgroups import cgroups
from automaxprocs.cgroups.cgroup import CGroup


@pytest.mark.parametrize("param", [{
    "subsys": cgroups._cgroupSubsysCPU,
    "path": "/sys/fs/cgroup/cpu,cpuacct",
}, {
    "subsys": cgroups._cgroupSubsysCPUAcct,
    "path": "/sys/fs/cgroup/cpu,cpuacct",
}, {
    "subsys": cgroups._cgroupSubsysCPUSet,
    "path": "/sys/fs/cgroup/cpuset",
}, {
    "subsys": cgroups._cgroupSubsysMemory,
    "path": "/sys/fs/cgroup/memory/large",
}])
def test_new_cgroups(param):
    testdata_proc_path = os.path.join(
        os.path.dirname(__file__), "../testdata", "proc")
    cgroups_proc_cgroup_path = os.path.join(
        testdata_proc_path, "cgroups", "cgroup")
    cgroups_proc_mount_info_path = os.path.join(
        testdata_proc_path, "cgroups", "mountinfo")

    cgroups_dict = cgroups.new_cgroups(
        cgroups_proc_mount_info_path,
        cgroups_proc_cgroup_path)
    cgroup = cgroups_dict[param["subsys"]]
    assert cgroup.path == param["path"]


@pytest.mark.parametrize("param",
                         [{"mountInfoPath": "non-existing-file",
                           "cgroupPath": "/dev/null",
                           },
                          {"mountInfoPath": "/dev/null",
                           "cgroupPath": os.path.join(os.path.dirname(__file__),
                                                      "../testdata",
                                                      "proc",
                                                      "invalid-cgroup",
                                                      "cgroup"),
                           },
                             {"mountInfoPath": os.path.join(os.path.dirname(__file__),
                                                            "../testdata",
                                                            "proc",
                                                            "invalid-mountinfo",
                                                            "mountinfo"),
                              "cgroupPath": "/dev/null"},
                             {"mountInfoPath": os.path.join(os.path.dirname(__file__),
                                                            "../testdata",
                                                            "proc",
                                                            "untranslatable",
                                                            "mountinfo"),
                              "cgroupPath": os.path.join(os.path.dirname(__file__),
                                                         "../testdata",
                                                         "proc",
                                                         "untranslatable",
                                                         "cgroup"),
                              }])
def test_new_cgroups_with_errors(param):
    cgroups_dict = cgroups.new_cgroups(
        param["mountInfoPath"], param["cgroupPath"])
    assert cgroups_dict is None


@pytest.mark.parametrize("param", [{
    "name": "cpu",
    "expectedQuota": 6.0,
    "expectedDefined": True,
    "shouldHaveError": False,
}, {
    "name": "undefined",
    "expectedQuota": -1.0,
    "expectedDefined": False,
    "shouldHaveError": False,
}, {
    "name": "undefined-period",
    "expectedQuota": -1.0,
    "expectedDefined": False,
    "shouldHaveError": True,
}])
def test_cgroups_cpu_quota(param):
    cgroups_dict = cgroups.CGroups()
    assert cgroups_dict == {}
    actual = cgroups_dict.cpu_quota()
    assert actual == (-1, False)

    cgroup_path = os.path.join(
        os.path.dirname(__file__),
        "../testdata/cgroups",
        param["name"])
    cgroups_dict[cgroups._cgroupSubsysCPU] = CGroup(cgroup_path)
    actual = cgroups_dict.cpu_quota()
    assert actual == (param["expectedQuota"], param["expectedDefined"])
