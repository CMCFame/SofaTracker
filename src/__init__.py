"""
Quiniela Tracker Initialization Module

This module ensures proper initialization of the package and imports necessary components.
"""

from .data_loader import QuinielaLoader
from .prediction_handler import PredictionManager
from .team_mappings import find_team_name

__all__ = [
    'QuinielaLoader',
    'PredictionManager',
    'find_team_name'
]