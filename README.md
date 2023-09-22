# private_values

Designed to use private data like username/pwd kept secure in OsEnvironment or IniFile for your several home projects at ones.  
And not open it in public.  
Main goals: short implementation and OOP usage.  

## Features
1. get values from:
   * Environment
   * iniFile
   * JsonFile

2. raise if no name in destination


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


## GUIDE

### 1. Env
* what a simple usage  
can use bot class- and object-method
```python
from private_values import *

class Cls:
   user = PrivateEnv.get("NameInEnv_ForUser")
   pwd = PrivateEnv().get("NameInEnv_ForPwd")
```

### 2. IniFile
* Use defaults (common usage)
```python
from private_values import *

class Cls:
   user = PrivateIni().get("NameInIni_ForUser")
   pwd = PrivateIni().get("NameInIni_ForPwd")
```

* Use different sections
```python
from private_values import *

class Cls:
   user = PrivateIni().get("NameInIni_ForUser")
   pwd = PrivateIni().get("NameInIni_ForPwd", _section="CustomSection")
```

* Change directory or filename or default section
```python
from private_values import *

class CustomIniValues(PrivateIni):
   DIRPATH = "new/path/"
   DIRPATH = pathlib.Path("new/path/")
   FILENAME = "my.ini"
   SECTION = "CustomSection"

class Cls:
   user = CustomIniValues.get("NameInIni_ForUser")
   pwd = CustomIniValues.get("NameInIni_ForPwd")
```

* Without creating new class
```python
from private_values import *

class Cls:
   pv1 = PrivateIni(_filename="otherFilename").get("pv1")
   pv2 = PrivateIni(_section="otherSection").get("pv2")
```

### 3. JsonFile
```python
from private_values import *

class Cls:
   user = PrivateJson().get("name1")
   pwd = PrivateIni().get("name2")
```
or by instance attributes
```python
# for Json
"""
{"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}
"""

from private_values import *

class MyPrivateJson(PrivateJson):
    SECTION = "AUTH"
    NAME: str
    PWD: str

class Cls:
    data = MyPrivateJson()
    def connect(self):
        name = self.data.NAME
        pwd = self.data.PWD
```
The same exists for PrivateIni

* use already created templates for standard attributes
```python
# for Json
"""
{"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}
"""

from private_values import *

class Cls:
    data = PrivateAuthJson().get(_section="AUTH")
    def connect(self):
        name = self.data.NAME
        pwd = self.data.PWD
```
