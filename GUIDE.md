# GUIDE

This guide is enough for most cases.  
Source code is small and pretty simple, good structured and self-documented. 
So feel free to take a look at source do discover some other implementation abilities which may be not so useful.


## 0. Suppose you already have next code

```python
class MyWork:
    user: str = "UserPrivate"
    pwd: str = "PwdPrivate"
```
It is contain private data - you can't push this in public place.


## 1. Change code

```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV___user: str = None
    PV___pwd: str = None
```
Now you can safely push it in any public repo.


## 2. Add default values

Use only string type! No other types like int/float.  
Don't place private data here!

```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV___user: str = "UserDemo"
    PV___pwd: str = "PwdDemo"
```

## 3. Add private values into appropriate hidden place

Notice: all names in source code must have prefix, and in original place (OsEnv/RcFile) it must have no prefix!  
For example above we need to add:
* user = "UserPrivate"
* pwd = "PwdPrivate"

This product gives you two abilities:
1. OsEnvironment - just add in environment as usual (ask google for you OS),
2. RcFile - standard Ini/Cfg format

```ini
user=UserPrivate  
pwd=PwdPrivate
```

## 4. Change rc-file dirpath or just name
```python
import pathlib
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV__RC_DIRPATH: Type_Path = pathlib.Path.home()
    PV__RC_FILENAME: str = ".pv_rc"
```

## 5. Disable using Env or Rc or even change Priority
```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV__ENV_BETTER_THEN_RC: bool = True
    
    PV__USE_ENV: bool = True
    PV__USE_RC: bool = True
```


## 6. Disable Exception

If you forgot to add some values, and it has not defval, 
you will get the Exception which notify you exact name on instance creation!  
If you don't need it (handle by your own), just disable it.
But don't forget it make sense only if any ENV has None value.

```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV___RISE_EXCEPTION_IF_NONE = False
```


## 7. Change attribute prefix

If default prefix is inappropriate for your project you can change it, but it is not recommended

```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV___PREFIX: str = "MyPrefix__"

    MyPrefix__user: str = None
    MyPrefix__pwd: str = None
```


## 8. Tips

You don't need to use it just like separated end class to handle only envs!  
Use nesting to any existed class.
Only special names of attributes will be updated from OsEnvironment.

```python
from private_values import PrivateValues


class MyWork(PrivateValues):
    PV___user: str = "UserDemo"
    PV___pwd: str = "PwdDemo"

    ATTR1 = 1
    ATTR2 = None

    def __init__(self):
        super().__init__()
        pass  # do smth

    def do_smth(self):
        pass  # do smth

```
