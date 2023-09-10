from setuptools import setup, find_packages

NAME = "private_values"

with open("README.md", "r") as f:
    readme = f.read()

setup(
  name=NAME,
  version="0.2.0.1",
  author="Andrei Starichenko",
  author_email="centroid@mail.ru",

  description="Update class attributes from OsEnvironment or IniFile",
  long_description=readme,
  long_description_content_type="text/markdown",
  keywords=["environs", "environment", "rc", "ini", "private", "test several 123"],

  # url="https://github.com/centroid457/private_values",
  project_urls={
    # "Documentation": "https://github.com/centroid457/private_values/blob/main/GUIDE.md",
    "Source": "https://github.com/centroid457/private_values",
  },

  packages=[NAME, ],
  install_requires=[],
  classifiers=[
    # "Framework :: ",
    "Topic :: Security",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Logging",
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Typing :: Typed",
  ],
  python_requires=">=3.6"
)
