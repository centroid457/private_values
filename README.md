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

See the [GUIDE](#GUIDE) to get main usage (that's enough for most cases).  
Source code is small and pretty simple, good structured and self-documented. 
So feel free to take a look at source do discover some other implementation abilities wich may be not so useful.



***

## GUIDE

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

Use only string type! no other types like int/float

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = "UserDemo"
    ENV__pwd: str = "PwdDemo"
```

### Don't forget to add envs to your OS

In our example we need this pair:
* ENV__user = "UserPrivate"
* ENV__pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  


### Disable Exception

If you forgot to add some of the envs into OS, and it has not defval, 
you will get the Exception which notify you exact env on instance creation!  
If you don't need it (handle by your own), just disable it.
But don't forget it make sense only if any ENV has None value.

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENVS_RISE_EXCEPTION = False
    
    ENV__user: str = "UserDemo"
    ENV__pwd: str = None
```


### You may change attribute prefix

if default prefix is inappropriate for your project you can change it, but it is not recommended

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENVS_PREFIX: str = "MyPrefix__"
    
    MyPrefix__user: str = None
    MyPrefix__pwd: str = None
```

In this case you need following env pair in your OS:
* MyPrefix__user = "UserPrivate"
* MyPrefix__pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  


### Environ names in OS and code source

In examples above you may notice that it is better to keep env names in OS as is 
and in your code just add prefix.
It is the best practice to get existed environs from OS. 
But if you need to add new ones there I think it is more preferable using name with prefix, 
so you can visually separate envs you specially add for python usage.


### Tips

You don't need use it just like separated end class to handle only envs!  
Use nesting to any existed class.
Only special names of attributes will be updated from OsEnvironment.

```python
from environs_os_getter_class import EnvsOsGetterClass

class MyWork(EnvsOsGetterClass):
    ENV__user: str = "UserDemo"
    ENV__pwd: str = "PwdDemo"

    ATTR1 = 1
    ATTR2 = None

    def __init__(self):
        super().__init__()
        # do smth

    def do_smth(self):
        # do smth
        pass
```
***