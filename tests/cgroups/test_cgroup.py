# -*- coding: utf-8 -*-

import os

import pytest
from automaxprocs.cgroups.cgroup import CGroup


def test_new_group():
    cgroup = CGroup("/sys/fs/cgroup/cpu")
    assert "/sys/fs/cgroup/cpu", cgroup.path()
    assert "/sys/fs/cgroup/cpu/cpu.cfs_quota_us", cgroup.param_path(
        "cpu.cfs_quota_us")


@pytest.mark.parametrize("param", [{
    "name": "cpu",
    "paramName": "cpu.cfs_period_us",
    "expectedContent": "100000",
    "shouldHaveError": False,
},
    {
    "name": "absent",
    "paramName": "cpu.stat",
    "expectedContent": "",
    "shouldHaveError": True,
},
    {
    "name": "empty",
    "paramName": "cpu.cfs_quota_us",
    "expectedContent": "",
    "shouldHaveError": True,
}])
def test_cgroup_read_first_line(param):
    testdata_path = os.path.join(os.path.dirname(__file__), "../testdata")
    cgroup_path = os.path.join(testdata_path, "cgroups", param["name"])
    cgroup = CGroup(cgroup_path)

    if not param["shouldHaveError"]:
        content = cgroup.read_first_line(param["paramName"])
        assert param["expectedContent"] == content
    else:
        try:
            cgroup.read_first_line(param["paramName"])
        except FileNotFoundError:
            pass


@pytest.mark.parametrize("param", [
    {
        "name": "cpu",
        "paramName": "cpu.cfs_period_us",
        "expectedContent": 100000,
        "shouldHaveError": False,
    },
    {
        "name": "empty",
        "paramName": "cpu.cfs_quota_us",
        "expectedContent": 0,
        "shouldHaveError": True,
    },
    {
        "name": "invalid",
        "paramName": "cpu.cfs_quota_us",
        "expectedContent": 0,
        "shouldHaveError": True,
    },
    {
        "name": "absent",
        "paramName": "cpu.cfs_quota_us",
        "expectedContent": 0,
        "shouldHaveError": True,
    }
])
def test_cgroup_read_int(param):
    testdata_path = os.path.join(os.path.dirname(__file__), "../testdata")
    cgroup_path = os.path.join(testdata_path, "cgroups", param["name"])
    cgroup = CGroup(cgroup_path)

    if not param["shouldHaveError"]:
        content = cgroup.read_int(param["paramName"])
        assert param["expectedContent"] == content
    else:
        try:
            cgroup.read_int(param["paramName"])
        except FileNotFoundError:
            pass
