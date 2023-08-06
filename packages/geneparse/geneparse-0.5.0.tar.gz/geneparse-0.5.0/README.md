[![PyPI version](https://badge.fury.io/py/geneparse.svg)](http://badge.fury.io/py/geneparse)
[![Build Status](https://travis-ci.org/pgxcentre/geneparse.svg?branch=master)](https://travis-ci.org/pgxcentre/geneparse)


# geneparse - Module to parse genetics data file

`geneparse` is a module that helps developers to parse multiple genetics file
format (*e.g.* Plink binary files, IMPUTE2 files and VCF).


## Dependencies

The tool requires a standard [Python](http://python.org/) installation (3.3 or
higher are supported) with the following modules:

1. [numpy](http://www.numpy.org/) version 1.11.0 or latest
2. [pandas](http://pandas.pydata.org/) version 0.19.0 or latest
3. [pyplink](https://github.com/lemieuxl/pyplink) version 1.3.4 or latest
4. [cyvcf2](https://github.com/brentp/cyvcf2) version 0.7.4 or latest
5. [biopython](https://github.com/biopython/biopython) version 1.68 or latest

The tool has been tested on *Linux* only, but should work on *MacOS* operating
systems as well.


## Installation

Using `pip`:

```bash
pip install geneparse
```


### Updating

To update the module using `pip`:

```bash
pip install -U geneparse
```


## Testing

To test the module, just perform the following command:

```console
$ python -m geneparse.tests
sssssss...ss.ss..............................
----------------------------------------------------------------------
Ran 45 tests in 0.395s

OK (skipped=11)
```
