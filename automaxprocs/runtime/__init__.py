# -*- coding: utf-8 -*-

import platform
if platform.system() == "Linux":
    from .cpu_quota_linux import cpu_quota_to_max_procs, cpu_request_to_max_procs
else:
    from .cpu_quota_unsupported import cpu_quota_to_max_procs, cpu_request_to_max_procs
