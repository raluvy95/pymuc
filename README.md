# Pymuc

a Python variant of original [muc](https://github.com/nate-sys/muc) for who simply don't want to use original Rust-based version.


# Installing

Your python version must have at least `3.10` to able to run it. Simply run `./pymuc -f $HISTFILE` or `./pymuc -h` to show list of arguments avaliable


Alternatively, use [pipenv](https://pipenv.pypa.io/en/latest/) if your distro doesn't ship with Python 3.10 yet.

```
$ pipenv install
$ pipenv run ./pymuch -f $HISTFILE
```