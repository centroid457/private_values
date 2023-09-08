# private_values


## Inspiration
Designed to use private data like username/pwd kept in OsEnvironment (or RcFile or even both variants) and not open it in public projects.  
Main goals: short implementation and OOP usage.  

So for your projects it helps you to share it in public and keep private data in secure.


## Features

1. Create classes with special attributes, which will be updated from OsEnvirons or RcFile.  
By default it must startswith PREFIX PV___.  
In case of OsEnvirons - it is very simple.  
For RcFile it gives you much more flexibility with ini-sections.

2. Ability to set default values.  
By this way you can share for example open username/pwd data, end user must create private data in the OS.

3. If finally no value withing any special attributes - raise Exception.  
You can disable this behaviour.


## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history

See the [HISTORY.md](HISTORY.md) file for release history.


## Help

See the [GUIDE.md](GUIDE.md) file for get started.


## Installation

```commandline
python pip install environs_os_getter_class
```

## Import

```python
from private_values import PrivateValues
```
