# -*- coding: utf-8 -*-
"""
UI Tab Mixins for LET IT DIE Save Editor.
Modular components dividing the editor GUI tabs into clean, maintainable units.
"""

from .currencies_tab import CurrenciesTabMixin
from .fighters_tab import FightersTabMixin
from .materials_tab import MaterialsTabMixin
from .decals_tab import DecalsTabMixin
from .blueprints_tab import BlueprintsTabMixin
from .mastery_tab import MasteryTabMixin
from .tower_tab import TowerTabMixin
from .advanced_tab import AdvancedTabMixin

__all__ = [
    "CurrenciesTabMixin",
    "FightersTabMixin",
    "MaterialsTabMixin",
    "DecalsTabMixin",
    "BlueprintsTabMixin",
    "MasteryTabMixin",
    "TowerTabMixin",
    "AdvancedTabMixin",
]
