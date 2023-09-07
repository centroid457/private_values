from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    readme = f.read()

setup(
  name='privet_values',
  version='0.0.3',
  author='Andrei Starichenko',
  author_email='centroid@mail.ru',
  description='Update class attributes from Os Environment',
  long_description=readme,
  long_description_content_type='text/markdown',
  url='https://github.com/centroid457/environs_os_getter_class',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.11',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
  ],
  keywords='environs environment rc privet',
  python_requires='>=3.6',
  project_urls={
    "Source": "https://github.com/centroid457/environs_os_getter_class",
  }
)
