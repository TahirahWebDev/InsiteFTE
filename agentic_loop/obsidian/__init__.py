"""
__init__.py for the obsidian module.
"""

from .api_wrapper import ObsidianAPIWrapper
from .dashboard import DashboardUpdater

__all__ = ['ObsidianAPIWrapper', 'DashboardUpdater']