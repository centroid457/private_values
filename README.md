![Ver/TestedPython](https://img.shields.io/pypi/pyversions/private_values)
![Ver/Os](https://img.shields.io/badge/os_development-Windows-blue)  
![repo/Created](https://img.shields.io/github/created-at/centroid457/private_values)
![Commit/Last](https://img.shields.io/github/last-commit/centroid457/private_values)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/private_values/actions/workflows/test_linux.yml/badge.svg)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/private_values/actions/workflows/test_windows.yml/badge.svg)  
![repo/Size](https://img.shields.io/github/repo-size/centroid457/private_values)
![Commit/Count/t](https://img.shields.io/github/commit-activity/t/centroid457/private_values)
![Commit/Count/y](https://img.shields.io/github/commit-activity/y/centroid457/private_values)
![Commit/Count/m](https://img.shields.io/github/commit-activity/m/centroid457/private_values)

# private_values (current v0.6.0/![Ver/Pypi Latest](https://img.shields.io/pypi/v/private_values?label=pypi%20latest))

## DESCRIPTION_SHORT
update values into class attrs from OsEnvironment or Ini/Json File

## DESCRIPTION_LONG
Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
    And not open it in public.  

    **CAUTION:**  
    in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.


## Features
1. load values to instance attrs from:  
	- Environment  
	- IniFile  
	- JsonFile  
	- CsvFile  
	- direct text instead of file  
	- direct dict instead of file  
2. attr access:  
	- via any lettercase  
	- by instance attr  
	- like dict key on instance  
3. work with dict:  
	- apply  
	- update  
	- preupdate  
4. update_dict as cumulative result - useful in case of settings result  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install private-values
```


## Import
```python
from private_values import *
```


********************************************************************************
## USAGE EXAMPLES
See tests, sourcecode and docstrings for other examples.  

------------------------------
### 1. example1.py
```python
# ===================================================================
# by instance attr
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME
        name = self.data.NamE     # case insensitive

# like dict key on instance
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data["NAME"]
        name = self.data["NamE"]   # case insensitive

# ===================================================================
### use annotations for your param names (best practice!)
# when instantiating if it will not get loaded these exact params from your private sources - RAISE!  
# but you could not use it and however keep access to all existed params in used section!
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *
class MyPrivateJson(PrivateJson):
    NAME: str
    PWD: str

name = MyPrivateJson().NAME


# ===================================================================
# in example above you could simply use existed classes
from private_values import *
name = PrivateAuthJson().NAME


# ===================================================================
### 1. Env

from private_values import *

class Cls:
   user = PrivateEnv["NAME"]
   user = PrivateEnv.NAME


# ===================================================================
### 2. IniFile
# Use different sections
from private_values import *
class Cls:
   user = PrivateIni(_section="CustomSection").NAME


# ===================================================================
# Change full settings
from private_values import *

class CustomIniValues(PrivateIni):
   DIRPATH = "new/path/"
   DIRPATH = pathlib.Path("new/path/")
   FILENAME = "my.ini"
   SECTION = "CustomSection"

class Cls:
   user = CustomIniValues.NAME

# ===================================================================
# Without creating new class
from private_values import *
class Cls:
   pv1 = PrivateIni(_filename="otherFilename").pv1


# ===================================================================
### 3. JsonFile
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class MyPrivateJson(PrivateJson):
    SECTION = "AUTH"
    NAME: str
    PWD: str

class Cls:
    data = MyPrivateJson()
    def connect(self):
        name = self.data.NAME

# ===================================================================
# use already created templates (PrivateAuthJson/PrivateTgBotAddressJson) for standard attributes
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME

# ===================================================================
### 4. Auto  
# you can use universal class  
# it will trying get all your annotated params from one source of Json/Ini/Env (in exact order)  
# in this case you cant use FileName and must use annotations!

# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class MyPrivate(PrivateAuto):
    SECTION = "AUTH"
    NAME: str
    PWD: str

name = MyPrivate().NAME
# ===================================================================
```

********************************************************************************
