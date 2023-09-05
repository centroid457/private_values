# environs_os_getter_class

***
## Inspiration
Designed to use private data like username/pwd kept in OsEnvironment and not open it in projects.  
Main goals: short implementation and OOP usage.


## Features
1. Create classes with special attributes, which will be updated from OS Environs.  
By default it must startswith "ENV__".

2. Ability to set default values.  
By this way you can share for example open username/pwd data, end user must create private data in the OS.

3. If finally no value withing any special attributes - raise Exception.  
You can disable this behaviour.

***
## Installation
```commandline
python pip install environs_os_getter_class
```

## Import
```python
from environs_os_getter_class import EnvsOsGetterClass
```
***
## Usage
You don't need use it like separated end class to handle only envs!  
Use nesting to any existed class.

### Before
Incorrect opened private data - cant push to public repo.
```python
class MyWork:
    user: str = "UserPrivate"
    pwd: str = "PwdPrivate"

```

### After
Now you need to add envs to your OS and can safely push in any public place!  
* ENV__user = "UserPrivate"
* ENV__pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  

If you forgot to add some envs, you will get the Exception which notify you exact env!  


```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = None
    ENV__pwd: str = None
```

Next you can add default public values.
```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = "UserDemo"
    ENV__pwd: str = "PwdDemo"
```
***