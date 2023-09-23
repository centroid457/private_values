import pip
from setuptools import setup, find_packages

pkgs = find_packages()
for pkg in pkgs:
    print(pkg)
pip.main(["install", "--upgrade", "NEW_PROJECT____"])


# EXIT PAUSE ==========================================================================================================
# input("press Enter to close")

import time
for i in range(3, 0, -1):
    print(f"exit in [{i}] seconds")
    time.sleep(1)


# =====================================================================================================================
