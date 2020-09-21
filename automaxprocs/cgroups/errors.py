# -*- coding: utf-8 -*-


class CgroupsException(Exception):
    pass


class CgroupSubsysFormatInvalidError(CgroupsException):
    def __init__(self, line, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line = line

    def __str__(self):
        return "invalid format for CGroupSubsys: %s" % self.line


class MountPointFormatInvalidError(CgroupsException):
    def __init__(self, line, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line = line

    def __str__(self):
        return "invalid format for MountPoint: %s" % self.line


class PathNotExposedFromMountPointError(CgroupsException):
    def __init__(self, mount_point, root, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mount_point = mount_point
        self.root = root
        self.path = path

    def __str__(self):
        return "path %s is not a descendant of mount point root %s and cannot be exposed from %s" % (
            self.path, self.root, self.mount_point)
