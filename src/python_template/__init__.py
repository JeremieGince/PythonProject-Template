"""
Project description.
"""

import importlib_metadata

__author__ = "Jeremie Gince"
__email__ = "gincejeremie@gmail.com"
__copyright__ = "Copyright 2024, Jeremie Gince"
__license__ = "Apache 2.0"
__url__ = "https://github.com/JeremieGince/PythonProject-Template"
__package__ = "python_template"
__version__ = importlib_metadata.version(__package__)

import warnings

warnings.filterwarnings("ignore", category=Warning, module="docutils")
warnings.filterwarnings("ignore", category=Warning, module="sphinx")
