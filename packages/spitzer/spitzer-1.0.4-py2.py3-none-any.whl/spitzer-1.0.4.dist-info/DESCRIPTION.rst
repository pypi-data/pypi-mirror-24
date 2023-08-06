# Spitzer

Django-based multi-target migration tool

# Install requires
- Python 3.4+
- Django
- PyYAML
- terminaltables
- cymysql
- django-cymysq

```PHP
pip install rinzler
```

# Config

Place a copy of the sample [spitzer.yaml](https://github.com/feliphebueno/Spitzer/wiki/spitzer.yaml) at 
your app's root directory.

# Usage
```PHP
//Configure e install Spitzer
$ python -m spitzer install

//Create and register a new blank migration file
$ python -m spitzer install

//Register your self-created migration file
$ python -m spitzer make_migrations

//Execute migrations on the configured target
$ python -m spitzer migrate

```


