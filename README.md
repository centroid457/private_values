# environs_os_getter_class


## Inspiration
Designed to use private data like username/pwd kept in OsEnvironment and not open it in public projects.  
Main goals: short implementation and OOP usage.


## Features

1. Create classes with special attributes, which will be updated from OS Environs.  
By default it must startswith PREFIX PV___.

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
from privet_values import PrivetValues
```
