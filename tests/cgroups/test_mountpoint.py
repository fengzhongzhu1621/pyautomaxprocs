# -*- coding: utf-8 -*-

import pytest
from automaxprocs.cgroups.mountpoint import (
    MountPoint, new_mount_point_from_line)


@pytest.mark.parametrize("param",
                         [{"name": "root",
                           "line": "1 0 252:0 / / rw,noatime - ext4 /dev/dm-0 rw,errors=remount-ro,data=ordered",
                           "expected": MountPoint(mount_id=1,
                                                  parent_id=0,
                                                  device_id="252:0",
                                                  root="/",
                                                  mount_point="/",
                                                  options=["rw", "noatime"],
                                                  optional_fields=[],
                                                  fs_type="ext4",
                                                  mount_source="/dev/dm-0",
                                                  super_options=["rw", "errors=remount-ro", "data=ordered"]),
                           },
                          {"name": "cgroup",
                           "line": "31 23 0:24 /docker /sys/fs/cgroup/cpu rw,nosuid,nodev,noexec,relatime shared:1 - cgroup cgroup rw,cpu",
                           "expected": MountPoint(mount_id=31,
                                                  parent_id=23,
                                                  device_id="0:24",
                                                  root="/docker",
                                                  mount_point="/sys/fs/cgroup/cpu",
                                                  options=["rw", "nosuid", "nodev", "noexec", "relatime"],
                                                  optional_fields=["shared:1"],
                                                  fs_type="cgroup",
                                                  mount_source="cgroup",
                                                  super_options=["rw", "cpu"]),
                           }
                          ])
def test_new_mount_point_from_line(param):
    subsys = new_mount_point_from_line(param["line"])
    assert subsys.__dict__ == param["expected"].__dict__
