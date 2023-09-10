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

```python
from private_values import *

class Cls:
    user = EnvValues.get("NameInEnv_ForUser")
    pwd = EnvValues.get("NameInEnv_ForPwd")
```

### 2. IniFile

* Use defaults

```python
from private_values import *

class Cls:
    user = IniValues.get("NameInIni_ForUser")
    pwd = IniValues.get("NameInIni_ForPwd")
```

* Use different sections

```python
from private_values import *

class Cls:
    user = IniValues.get("NameInIni_ForUser")
    pwd = IniValues.get("NameInIni_ForPwd", section="CustomSection")
```

* Change directory or filename or default section

str and pathlib are accepted

```python
from private_values import *

class CustomIniValues(IniValues):
    DIRPATH = "new/path/"
    FILENAME = "my.ini"
    SECTION = "CustomSection"

class Cls:
    user = CustomIniValues.get("NameInIni_ForUser")
    pwd = CustomIniValues.get("NameInIni_ForPwd")
```

### 3. disable Exceptions

`_raise_exx` is useful in all *.get methods for both classes

```python
from private_values import *

class Cls:
    user = EnvValues.get("Name_ForUser", _raise_exx=False)
    pwd = IniValues.get("Name_ForPwd", _raise_exx=False)

    def connect(self):
        if None in [self.user, self.pwd]:
            return
        pass

```
