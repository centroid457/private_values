# environs_os_getter_class

## Inspiration
Designed to use private data like username/pwd kept in OsEvironment and not open it in projects.

## Features
1. Create classes with special attributes, wich will be updated from OS Environs.  
By default it must startswith "ENV__".
2. Ability to set default values.  
By this way you can share for example open username/pwd data, end user must create private data in the OS.
3. if finally no value withing any special attributes - raise Exception.  
You can disable this behaviour.

## Installation
```commandline
python pip install environs_os_getter_class
```

## Import
```python
from environs_os_getter_class import EnvironsOsGetterClass
```

## Usage

```python
class MyClassWithEnvs(EnvironsOsGetterClass):
    ENV__env1_without_defval: str = None
    ENV__env2_with_defval: str = "env2_defval"

```
