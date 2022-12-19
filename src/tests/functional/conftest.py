import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
pytest_plugins = [
    "fixtures.fixture",
]
