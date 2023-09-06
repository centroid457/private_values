# environs_os_getter_class

## INFORMATION


### Inspiration
Designed to use private data like username/pwd kept in OsEnvironment and not open it in public projects.  
Main goals: short implementation and OOP usage.


### Features

1. Create classes with special attributes, which will be updated from OS Environs.  
By default it must startswith "ENV__".

2. Ability to set default values.  
By this way you can share for example open username/pwd data, end user must create private data in the OS.

3. If finally no value withing any special attributes - raise Exception.  
You can disable this behaviour.


### License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


### Release history

See the [HISTORY.md](HISTORY.md) file for release history.


### Help

Source code is small and pretty simple, good structured and self-documented. 
So feel free to take a look at source do discover implementation abilities. 



***
## QUICK START

### Installation

```commandline
python pip install environs_os_getter_class
```

### Import

```python
from environs_os_getter_class import EnvsOsGetterClass
```

### Suppose you have at start next code

Opened private data - cant push to public repo.

```python
class MyWork:
    user: str = "UserPrivate"
    pwd: str = "PwdPrivate"
```

### Change code

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = None
    ENV__pwd: str = None
```
Now you can safely push it in any public repo.


### Add default (public) values

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = "UserDemo"
    ENV__pwd: str = "PwdDemo"
```

### Dont forget to add envs to your OS

In our example you need this pair:
* ENV__user = "UserPrivate"
* ENV__pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  


### Disable Exception

If you forgot to add some of the envs into OS and it have not defval, you will get the Exception which notify you exact env on instance creation!  
If you dont need it (handle by your own), just disable it

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENVS_RISE_EXCEPTION = False
    
    ENV__user: str = "UserDemo"
    ENV__pwd: str = None
```


### Tips

You don't need use it just like separated end class to handle only envs!  
Use nesting to any existed class.

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENVS_RISE_EXCEPTION = False
    
    ENV__user: str = "UserDemo"
    ENV__pwd: str = "PwdDemo"

    ATTR1 = 1
    ATTR2 = 2

    def __init__(self):
        super().__init__()
        
        # do smth

    def do_smth(self):
        # do smth
        pass
```
***