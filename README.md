# `beditor`

[![build status](
  http://img.shields.io/travis/rraadd88/beditor/master.svg?style=flat)](
 https://travis-ci.org/rraadd88/beditor) [![PyPI version](https://badge.fury.io/py/beditor.svg)](https://pypi.python.org/pypi/beditor)

Datasets used by Travis Continuous-Integration platform (https://travis-ci.org/).

## Usage

### Cloning the repository:

    git clone https://github.com/rraadd88/test_beditor.git

    
### For testing options of beditor:

    source activate beditor;cd test_beditor;python test_datasets.py

### For testing different species (example human,yeast and fish). 

Note: this testing would download genomes of species which would take >50 Giga bytes and may take a long while to finish.  

    source activate beditor;cd test_beditor;python make_datasets.py

It will create directories with a prefix 'dataset_'. Then individual species can be tested by commands in following format.

    source activate beditor;cd test_beditor/dataset_{species name};beditor --cfg {name of the .yml file}

Usage
-----

1.  Run the analysis.

``` {.sourceCode .text}
beditor --cfg configuration.yml
```

2.  Run a single step in the analysis.

``` {.sourceCode .text}
beditor --cfg --step {step number} configuration.yml
```
`step number` and corresponding analysis:

``` {.sourceCode .text}
1: Get genomic loci flanking the target site
2: Get possible mutagenesis strategies
3: Design guides
4: Check offtarget-effects
``` 

3. To list existing pams and editors

``` {.sourceCode .text}
beditor --list pams
beditor --list editors
```

4. Help

``` {.sourceCode .text}
beditor --help
```

Input format
------------------

Input [1/2]: Configuration file. It contains all the options and paths to files needed by the analysis. 
This YAML formatted file contains the all the analysis specific parameters.

Template:
<https://github.com/rraadd88/test_beditor/blob/master/common/configuration.yml>

```
# Input: Mutation information
## Path to this tsv (tab-separated values) file
dinp: input.tsv
reverse_mutations: False

# Step 1: Extracting sequences flanking mutation site (`01_sequences/`).
## host information
host: scientific name
genomerelease: 93
# check assembly from http://useast.ensembl.org/index.html
genomeassembly: fromensembl


# Step 2: Estimating the editable mutations based on base editors chosen. (`02_mutagenesis/`).
# whether aminoacid or nucleotide mutations
mutation_format: aminoacid or nucleotide
##[N nonsyn] S syn else both
mutation_type: N
## keep nonsense mutations
keep_mutation_nonsense: False
## Mutations information can be provided in 3 options: 
## 1. Required Mutations mentioned in input file. 
## 2. Required Substitutions provided as a file (template: https://github.com/rraadd88/test_beditor/blob/master/common/dsubmap.tsv).
## 3. Carry out Mimetic substitutions (base on genome wide substitution maps). Only for human and yeast.
## input: options 
## mutations: 1, substitutions: 2, mimetic: 3, [no input: keeps all possible mutations (slow)]
mutations: 1
## Parameters specific to above options
## 2. Substitutions provided as a file
dsubmap_preferred_path: 
## 3. Mimetic substitutions
## mimetism level (high: only the best one, [medium: best 5], low: best 10)
mimetism_level: medium
## can not mutate between these 
## if ['S','T','K'] is provided all mutations between thsese amino acids are disallowed
non_intermutables: []


# Step 3: Designed guides (`03_guides/`).
## allowed nucleuotide substitutions per codon
max_subs_per_codon: 1
## base editors to use (restriction max_subs_per_codon would override the choice of base editors)
BEs: ['Target-AID','ABE']
# Cas9 related options
## PAM sequence
pams: ['NGG','NG']

#------------------------------------------------
# System related options 
## Number of cpus/threads
cores: 6
## Number of lines to process per cpu
chunksize: 200
## Dependencies 
## by default the dependencies are installed from the conda environment.
## "optionally" paths to the dependencies could be included below.
bedtools: bedtools
bwa: bwa
samtools: samtools
```

Input [2/2]: Table with mutation information.  

Note: Path to this tsv (tab-separated values) file is provided in configuration file as a value for variable called `dinp`. E.g. `dinp: input.tsv`. 

According to the mutation_format opted in configuration.yml file and corresponding columns needed in input.

### nucleotide : ['genome coordinate','nucleotide mutation'].

Example:

| genome coordinate | nucleotide mutation |
|-------------------|---------------------|
| II:711491-711491+ | T                   |
| II:712904-712904- | T                   |
| II:714707-714707- | G                   |
| II:716782-716782- | G                   |

### aminoacid  : ['transcript: id','aminoacid: position','amino acid mutation'].

Example:

| transcript: id | aminoacid: position | amino acid mutation |
|----------------|---------------------|---------------------|
| YAL040C        | 6                   | A                   |
| YAL041W        | 18                  | A                   |
| YAL042C-A      | 65                  | A                   |
| YAL042W        | 3                   | C                   |
| YAL043C        | 14                  | C                   |
