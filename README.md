# private_values


Designed to use private data like username/pwd kept secure in OsEnvironment or IniFile for your several home projects at ones.  
And not open it in public.  
Main goals: short implementation and OOP usage.  


## Features

1. get values from:
   * Environment
   * iniFile

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

str and pathlib are accepted

```python
from private_values import *

class CustomIniValues(PrivateIni):
   DIRPATH = "new/path/"
   FILENAME = "my.ini"
   SECTION = "CustomSection"

class Cls:
   user = CustomIniValues.get("NameInIni_ForUser")
   pwd = CustomIniValues.get("NameInIni_ForPwd")
```

### 3. Without creating new class
```python
from private_values import *

class Cls:
   pv1 = PrivateIni(_filename="otherFilename").get("pv1")
   pv2 = PrivateIni(_section="otherSection").get("pv2")
```

### 4. disable Exceptions

* in method

`_raise_exx` is useful in all *.get methods for both classes

```python
from private_values import *

class Cls:
   user = PrivateEnv().get("Name_ForUser", _raise_exx=False)
   pwd = PrivateIni().get("Name_ForPwd", _raise_exx=False)

   def connect(self):
      if None in [self.user, self.pwd]:
         return
      pass
```

* in whole class

`_raise_exx` is useful in all *.get methods for both classes

```python
from private_values import *

class CustomEnvValues(PrivateEnv):
   RAISE_EXX = False

class CustomIniValues(PrivateIni):
   RAISE_EXX = False

class Cls:
   user = CustomEnvValues.get("Name_ForUser")
   pwd = CustomIniValues.get("Name_ForPwd")

   def connect(self):
      if None in [self.user, self.pwd]:
         return
      pass
```