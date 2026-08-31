"""
Root conftest.py — adds the project root to sys.path so pytest can
import src.* modules without needing src/__init__.py or an editable install.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
