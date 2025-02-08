# Copyright (c) 2025 Marcin Zdun
# This code is licensed under MIT license (see LICENSE for details)

"""
The **proj_flow.ext.markdown_changelist** .
"""

from proj_flow.log.rich_text.api import changelog_generators
from proj_flow.log.rich_text.markdown import ChangelogGenerator


@changelog_generators.add
class Plugin(ChangelogGenerator):
    pass
