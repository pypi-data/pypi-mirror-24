# VisiData v0.96 [![CircleCI](https://circleci.com/gh/saulpw/visidata/tree/stable.svg?style=svg)](https://circleci.com/gh/saulpw/visidata/tree/stable)

A terminal interface for exploring and arranging tabular data

<a href="https://github.com/saulpw/visidata/blob/develop/docs/tours.rst">![VisiData silent demo](docs/img/birdsdiet_bymass.gif)</a>

A few interesting commands:

* `Shift-F` pushes a frequency analysis of the current column
* `=` creates a new column from the given Python expression (use column names to refer to their contents)
* `;` creates new columns from the match groups of the given regex

# Getting Started

## Install VisiData

### from pypi (`stable` branch)

```
$ pip3 install visidata
```

### or clone from git

```
$ git clone http://github.com/saulpw/visidata.git
$ cd visidata
$ pip install -r requirements.txt
$ python setup.py install
```

### Dependencies

- Python 3.3+
- h5py and numpy (if opening .hdf5 files)

**Remember to install the Python3 versions of these packages with e.g. `pip3`**

## Run VisiData

If installed via pip3, `vd` should launch without issue.

```
$ vd [<options>] <input> ...
$ <command> | vd
$ vd [<options>] --play <script.vd> [--<format-field>=<value> ...]
$ vd [<options>] --play - [--<format-field>=<value> ...] < <script.vd>
$ vd [<options>] < <input>
```

If no inputs are given, `vd` opens the current directory.
Unknown filetypes are by default viewed with a text browser.

If installed via `git clone`, first set up some environment variables (on terminal):

```
$ export PYTHONPATH=<visidata_dir>:$PYTHONPATH
$ export PATH=<visidata_dir>/bin:$PATH
```

Further documentation is available at [readthedocs](https://visidata.readthedocs.io/).

## Contributing

VisiData was created by Saul Pwanson `<vd@saul.pw>`.

VisiData needs lots of usage and testing to help it become useful and reliable.
If you use VisiData, I would love it if you would send me a screencast!
Maybe there is an easy way to improve the tool for both of us.

Also please create a GitHub issue if anything doesn't appear to be working right.
If you get an unexpected error, please include the full stack trace that you get with `Ctrl-e`.

### Branch structure

VisiData has two main branches:
* [stable](https://github.com/saulpw/visidata/tree/stable) has the last known good version of VisiData (which should be on pypi).
* [develop](https://github.com/saulpw/visidata/tree/develop) has the most up-to-date version of VisiData (which will eventually be merged to stable).

If you wish to contribute, please fork from [develop](https://github.com/saulpw/visidata/tree/develop) and submit a [pull request](https://github.com/saulpw/visidata/pulls) against it.

A developer's guide can be found [here](http://visidata.readthedocs.io/en/stable/architecture.html).

## License

The innermost core file, `vdtui.py`, is a single-file stand-alone library that provides a solid framework for building text user interface apps. It is distributed under the MIT free software license, and freely available for inclusion in other projects.

Other VisiData components, including the main `vd` application, addons, and other code in this repository, are licensed under GPLv3.
