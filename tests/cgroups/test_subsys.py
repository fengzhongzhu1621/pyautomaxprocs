# -*- coding: utf-8 -*-

import pytest
from automaxprocs.cgroups.subsys import (
    CGroupSubsys, new_cgroup_subsys_from_line)


@pytest.mark.parametrize("test_table_item", [
    {
        "name": "single-subsys",
        "line": "1:cpu:/",
        "expectedSubsys": CGroupSubsys(
            subsys_id=1,
            subsystems=["cpu"],
            name="/"
        ),
    },
    {
        "name": "multi-subsys",
        "line": "8:cpu,cpuacct,cpuset:/docker/1234567890abcdef",
        "expectedSubsys": CGroupSubsys(
            subsys_id=8,
            subsystems=["cpu", "cpuacct", "cpuset"],
            name="/docker/1234567890abcdef"
        ),
    },
])
def test_new_cgroup_subsys_from_line(test_table_item):
    subsys = new_cgroup_subsys_from_line(test_table_item["line"])
    assert subsys.id == test_table_item["expectedSubsys"].id
    assert subsys.subsystems == test_table_item["expectedSubsys"].subsystems
    assert subsys.name == test_table_item["expectedSubsys"].name
