# -*- coding: utf-8 -*-

import os
from typing import List, Callable
from .errors import (
    PathNotExposedFromMountPointError,
    MountPointFormatInvalidError)


_mountInfoSep = " "
_mountInfoOptsSep = ","
_mountInfoOptionalFieldsSep = "-"


_miFieldIDMountID = 0
_miFieldIDParentID = 1
_miFieldIDDeviceID = 2
_miFieldIDRoot = 3
_miFieldIDMountPoint = 4
_miFieldIDOptions = 5
_miFieldIDOptionalFields = 6
_miFieldCountFirstHalf = 7


_miFieldOffsetFSType = 0
_miFieldOffsetMountSource = 1
_miFieldOffsetSuperOptions = 2
_miFieldCountSecondHalf = 3

_miFieldCountMin = _miFieldCountFirstHalf + _miFieldCountSecondHalf


class MountPoint:
    """
    MountPoint is the data structure for the mount points in
    `/proc/$PID/mountinfo`. See also proc(5) for more information.
    """

    def __init__(
            self,
            mount_id: int,
            parent_id: int,
            device_id: str,
            root: str,
            mount_point: str,
            options: List[str],
            optional_fields: List[str],
            fs_type: str,
            mount_source: str,
            super_options: List[str]):
        self.mount_id = mount_id
        self.parent_id = parent_id
        self.device_id = device_id
        self.root = root
        self.mount_point = mount_point
        self.options = options
        self.optional_fields = optional_fields
        self.fs_type = fs_type
        self.mount_source = mount_source
        self.super_options = super_options

    def translate(self, abs_path: str) -> str:
        rel_path = os.path.relpath(abs_path, self.root)

        if rel_path == ".." or rel_path.startswith("../"):
            raise PathNotExposedFromMountPointError(
                self.mount_point, self.root, self.path)

        return os.path.join(self.mount_point, rel_path)


def new_mount_point_from_line(line: str) -> MountPoint:
    fields = line.split(_mountInfoSep)

    if len(fields) < _miFieldCountMin:
        raise MountPointFormatInvalidError(line)

    mount_id = int(fields[_miFieldIDMountID])
    parent_id = int(fields[_miFieldIDParentID])

    for i, field in enumerate(fields[_miFieldIDOptionalFields:]):
        if field == _mountInfoOptionalFieldsSep:
            fs_type_start = _miFieldIDOptionalFields + i + 1
            if len(fields) != fs_type_start + _miFieldCountSecondHalf:
                raise MountPointFormatInvalidError(line)

            mi_field_id_fs_type = _miFieldOffsetFSType + fs_type_start
            mi_field_id_mount_source = _miFieldOffsetMountSource + fs_type_start
            mi_field_id_super_options = _miFieldOffsetSuperOptions + fs_type_start

            mount_point = MountPoint(
                mount_id=mount_id,
                parent_id=parent_id,
                device_id=fields[_miFieldIDDeviceID],
                root=fields[_miFieldIDRoot],
                mount_point=fields[_miFieldIDMountPoint],
                options=fields[_miFieldIDOptions].split(_mountInfoOptsSep),
                optional_fields=fields[_miFieldIDOptionalFields:(fs_type_start - 1)],
                fs_type=fields[mi_field_id_fs_type],
                mount_source=fields[mi_field_id_mount_source],
                super_options=fields[mi_field_id_super_options].split(_mountInfoOptsSep)
            )
            return mount_point


def parse_mount_info(proc_path_mount_info: str, new_mount_point: Callable[[MountPoint], None]):
    with open(proc_path_mount_info) as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            mount_point = new_mount_point_from_line(line)
            new_mount_point(mount_point)
