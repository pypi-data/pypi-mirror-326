# Copyright (c) 2025 Marcin Zdun
# This code is licensed under MIT license (see LICENSE for details)

"""
The **proj_flow.plugins.cmake.pack** provides ``"Pack"`` step.
"""

import os

from proj_flow.api import env, step

from .__version__ import CMAKE_VERSION


@step.register
class PackStep:
    """
    Packs archives and installers from ``cpack_generator`` config, using
    ``preset`` config.
    """

    name = "Pack"
    runs_after = ["Build"]

    def platform_dependencies(self):
        return [f"cmake>={CMAKE_VERSION}", f"cpack>={CMAKE_VERSION}"]

    def is_active(self, config: env.Config, rt: env.Runtime) -> int:
        return (
            os.path.isfile("CMakeLists.txt")
            and os.path.isfile("CMakePresets.json")
            and len(config.items.get("cpack_generator", [])) > 0
        )

    def run(self, config: env.Config, rt: env.Runtime) -> int:
        generators = ";".join(config.items.get("cpack_generator", []))
        return rt.cmd("cpack", "--preset", config.preset, "-G", generators)
