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
    """解析文件系统挂载信息

    字段详情：https://man7.org/linux/man-pages/man5/proc.5.html
    """
    # 分割每一行
    fields = line.split(_mountInfoSep)
    # 每一行有至少10个属性，可能大于10个
    if len(fields) < _miFieldCountMin:
        raise MountPointFormatInvalidError(line)
    # 第0列：mount ID,挂载点的唯一标识
    mount_id = int(fields[_miFieldIDMountID])
    # 第1列：parent ID,当前挂载点的父挂载点的ID
    parent_id = int(fields[_miFieldIDParentID])
    # 第2列：major:minor, files的st_dev的值
    # 第3列：root: 文件系统的根挂载点
    # 第4列：mount point: 相对于进程根目录的挂载点
    # 第5列：mount options: 预挂载选项
    # 第6列：options fields: tag:[value]类型的字段

    for i, field in enumerate(fields[_miFieldIDOptionalFields:]):
        # 第7列：sparator: options fields结束标志
        if field == _mountInfoOptionalFieldsSep:
            fs_type_start = _miFieldIDOptionalFields + i + 1
            if len(fields) != fs_type_start + _miFieldCountSecondHalf:
                raise MountPointFormatInvalidError(line)
            # 第8列：file systemtype: 文件系统的名称,以type[.subtype]的方式命名
            mi_field_id_fs_type = _miFieldOffsetFSType + fs_type_start
            # 第9列：mount source: 文件特定信息
            mi_field_id_mount_source = _miFieldOffsetMountSource + fs_type_start
            # 第10列：super options: 超级块选项
            mi_field_id_super_options = _miFieldOffsetSuperOptions + fs_type_start

            # 创建文件系统挂载点对象
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
    """解析挂载的文件系统信息

    Args:
        proc_path_mount_info(str): 当前系统所有挂载文件系统的信息
        new_mount_point: 每一个挂载的文件系统的解析回调
    """
    with open(proc_path_mount_info) as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            # 解析每一个挂载的文件系统的信息，返回文件系统挂载点对象
            mount_point = new_mount_point_from_line(line)
            # 执行回调
            new_mount_point(mount_point)
