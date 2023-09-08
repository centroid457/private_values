# GUIDE

This guide is enough for most cases.  
Source code is small and pretty simple, good structured and self-documented. 
So feel free to take a look at source do discover some other implementation abilities which may be not so useful.


## Suppose you already have next code

```python
class MyWork:
    user: str = "UserPrivate"
    pwd: str = "PwdPrivate"
```
It is contain private data - you can't push this in public place.


## Change code

```python
from privet_values import PrivetValues


class MyWork(PrivetValues):
    PV___user: str = None
    PV___pwd: str = None
```
Now you can safely push it in any public repo.


## Add default values

Use only string type! No other types like int/float.  
Don't place private data here!

```python
from privet_values import PrivetValues


class MyWork(PrivetValues):
    PV___user: str = "UserDemo"
    PV___pwd: str = "PwdDemo"
```

## Add envs to your OS

In our example we need this pair:
* PV___user = "UserPrivate"
* PV___pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  


## Disable Exception

If you forgot to add some of the envs into OS, and it has not defval, 
you will get the Exception which notify you exact env on instance creation!  
If you don't need it (handle by your own), just disable it.
But don't forget it make sense only if any ENV has None value.

```python
from privet_values import PrivetValues


class MyWork(PrivetValues):
    PV___RISE_EXCEPTION_IF_NONE = False

    PV___user: str = "UserDemo"
    PV___pwd: str = None
```


## Change attribute prefix

If default prefix is inappropriate for your project you can change it, but it is not recommended

```python
from privet_values import PrivetValues


class MyWork(PrivetValues):
    PV___PREFIX: str = "MyPrefix__"

    MyPrefix__user: str = None
    MyPrefix__pwd: str = None
```

In this case you need following env pair in your OS:
* MyPrefix__user = "UserPrivate"
* MyPrefix__pwd = "PwdPrivate"  
or
* user = "UserPrivate"
* pwd = "PwdPrivate"  


## Environ names in OS and code source

In examples above you may notice that it is better to keep env names in OS as is 
and in your code just add prefix.
It is the best practice to get existed environs from OS. 
But if you need to add new ones there I think it is more preferable using name with prefix, 
so you can visually separate envs you specially add for python usage.


## Tips

You don't need use it just like separated end class to handle only envs!  
Use nesting to any existed class.
Only special names of attributes will be updated from OsEnvironment.

```python
from privet_values import PrivetValues


class MyWork(PrivetValues):
    PV___user: str = "UserDemo"
    PV___pwd: str = "PwdDemo"

    ATTR1 = 1
    ATTR2 = None

    def __init__(self):
        super().__init__()
        pass    # do smth

    def do_smth(self):
        pass    # do smth

```
