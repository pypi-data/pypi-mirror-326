# Copyright (c) 2025 Marcin Zdun
# This code is licensed under MIT license (see LICENSE for details)

"""
The **proj_flow.plugins.commands** package implements various CLI commands.
"""

import sys

from proj_flow.base.plugins import load_module_plugins

load_module_plugins(sys.modules[__name__])
