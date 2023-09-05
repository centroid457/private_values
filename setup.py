from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    readme = f.read()

setup(
  name='environs_os_getter_class',
  version='1.0.0',
  author='Andrei Starichenko',
  author_email='centroid@mail.ru',
  description='Update class attributes from Os Environment',
  long_description=readme,
  long_description_content_type='text/markdown',
  url='https://github.com/centroid457/environs_os_getter_class',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Natural Language :: English',
  ],
  keywords='example python',
  python_requires='>=3.6',
  zip_safe=False
)

