# `beditor`

[![build status](
  http://img.shields.io/travis/rraadd88/beditor/master.svg?style=flat)](
 https://travis-ci.org/rraadd88/beditor) [![PyPI version](https://badge.fury.io/py/beditor.svg)](https://pypi.python.org/pypi/beditor)

Datasets used by Travis Continuous-Integration platform (https://travis-ci.org/).

## Usage
    
### For testing options of beditor:

    source activate beditor;cd test_beditor;python test_datasets.py

### For testing different species (human,fish,yeast and worm). 
Note: this testing would download genomes of species which would take >50 Giga bytes and may take a long while to finish.  

    source activate beditor;cd test_beditor;python make_datasets.py

It will create directories with a prefix 'dataset_'. Then individual species can be tested by commands in following format.

    source activate beditor;cd test_beditor/dataset_{species name};beditor --cfg {name of the .yml file}
