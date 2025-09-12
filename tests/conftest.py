import os
import sys
# Ensure repository root is on sys.path for 'app' imports when running pytest with absolute paths
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
