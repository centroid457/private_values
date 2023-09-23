# private_values

Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
And not open it in public.


## Features
1. load values to instance attrs from:
   * Environment
   * iniFile
   * JsonFile
2. attr acess
   * via any lettercase  
   see below
   * by instanse attr
```python
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME
        name = self.data.NamE     # case insensitive
```
  * like dict key on instance  
```python
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data["NAME"]
        name = self.data["NamE"]   # case insensitive
```


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
```python
from private_values import *

class Cls:
   user = PrivateEnv["NAME"]
   user = PrivateEnv.NAME
```

### 2. IniFile
* Use defaults (common usage)
```python
from private_values import *

class Cls:
   user = PrivateIni().NAME
```

* Use different sections
```python
from private_values import *

class Cls:
   user = PrivateIni(_section="CustomSection").NAME
```

* Change full settings
```python
from private_values import *

class CustomIniValues(PrivateIni):
   DIRPATH = "new/path/"
   DIRPATH = pathlib.Path("new/path/")
   FILENAME = "my.ini"
   SECTION = "CustomSection"

class Cls:
   user = CustomIniValues.NAME
```

* Without creating new class
```python
from private_values import *

class Cls:
   pv1 = PrivateIni(_filename="otherFilename").pv1
```

### 3. JsonFile
```python
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
```

* use already created templates (PrivateAuthJson/PrivateTgBotAddressJson) for standard attributes
```python
# {"AUTH": {"NAME": "MyName", "PWD": "MyPwd"}}

from private_values import *

class Cls:
    data = PrivateAuthJson(_section="AUTH")
    def connect(self):
        name = self.data.NAME
```
