# `beditor`

Python package to design guides for CRISPR base editing. 

## Requirements

1. Ubuntu 16.04 and 14.04 (64 bit).

2. Python 3.6.5 and Anaconda package distributor. A virtual environment can be created from environment.yml file in the repo.
	
	cd beditor
	conda env create -f environment.yml

3. For now, one of the required package called `pyensembl` need to installed by following command.

	pip install https://github.com/rraadd88/pyensembl/archive/master.zip

## Instalation

The package can be installed by following commands depending on your need.

1. For stable versions:

	```
	source activate beditor # activates the virtual environment (python 3.6.5)
	pip install beditor
	```

2. For latest developments:

Clone the [gihub repo](http://github.com/rraadd88/beditor.git). 

	```
	git clone http://github.com/rraadd88/beditor.git
	```
	
	To install the package,

	```
	cd beditor
	source activate beditor # activates the virtual environment (python 3.6.5)
	pip install -e .
	```

	To update the package,

	```
	cd beditor
	git pull
	```	

## Analysis workflow

There are 4 steps of analysis:

1. Extracting sequences (-21[3 codon bases]+21) flanking a codon position, from genome.
2. Estimating the editable mutations based on base editors choosed.
3. Designing guides.
4. Checking offtarget effects.

## Usage

To run all the steps in tandem,

	beditor --cfg config.yml 

To run a single step,

	beditor --step {step number} --cfg config.yml 

Here, `config.yml` is a configuration file that contains all the input parameters needed for the analysis.

To list supported pams and editors

	beditor --list pams
	beditor --list editors

These lists are located in `beditor/data` folder and can be modified. 

## Configuration

1. Make a configuration `yaml` file (see test.yml for example)

This file contains all the input parameters needed for the analysis:

	# input file path
	dinp: input.tsv

	#common crispr params
	#guidel: 23
	pams: ['NGG','NG']

	#common 
	## cpus/threads
	cores: 6
	## number of lines to process per cpu
	chunksize: 40

	# 01_sequences
	## host information
	host: scientific name
	genomerelease: 92
	# check assembly from http://useast.ensembl.org/index.html
	genomeassembly: fromensembl

	# 02_mutations
	##[N nonsyn] S syn else both
	mutation_type: N
	## keep nonsense
	keep_mutation_nonsense: False
	## allowed nucleuotide substitutions per codon
	max_subs_per_codon: 1
	## base editors to use (restriction max_subs_per_codon would override the choice of base editors)
	BEs: ['Target-AID','ABE']

	## Mutations information can be provided in 3 options: 
	## 1. Required Mutations mentioned in input file (in a column called "amino acid mutation") would override this 
	## 2. Required Substitutions provided as a file
	## 3. Carry out Mimetic substitutions (base on genome wide substitution maps). Only for human and yeast.
	## input: options 
	## mutations: 1, substitutions: 2, mimetic: 3, [no input: keeps all possible mutations (slow)]
	mutations: 

	## Option specific options
	## 2. Substitutions provided as a file
	dsubmap_preferred_path: 

	## 3. Mimetic substitutions
	## mimetism level (high: only the best one, [medium: best 5], low: best 10)
	mimetism_level: medium

	## can not mutate between these 
	# non_intermutables: ['S','T','K']

	## 04offtargets
	mismatches_max: 3

## Outputs
	
A directory by the basename of configuration file (eg. directory called 'human' if configuration file is 'human.yml') would be created in the same folder where configuration file is located. It is referred to as 'project directory'.

Inside a project directory there would be following folders named by corresponding steps of analysis.

1. `01_sequences/`
Stores the output of step #1. Extracting sequences (-21[3 codon bases]+21) flanking a codon position, from genome.
2. `02_mutagenesis/`
Stores the output of step #2. Estimating the editable mutations based on base editors choosed.
3. `03_guides/`
Stores the output of step #3. Designing guides.
4. `04_offtargets/`
Stores the output of step #4. Checking offtarget effects.

Also,
- `00_input/`
Store the input files.
- `chunks/`
If parallel processing is used, this folder would store the individual parts (chunks) of the analysis. 

## Test datasets

	cd test_dataset
	cd {organism name}
	beditor --cfg project_name_all.yml

#TODOs
## Visualizations

1. Individual mutation #TODO

Shows all the possible ways a mutation can be carried out. Also creates a genebank file.

2. Cumulative #TODO
2.1 A distribution plot guides 
x axis nucleiotide position 
x counts of nucleiotides
shows guides on both the strands

in columns: type of pam used
in subrows: type of pam
in rows: position of editing

2.2 bar plot by strategies (guides per NG, NGG etc) 
