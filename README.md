# `beditor`

Python package to design guides for CRISPR base editing. 

## Requirements

1. Ubuntu 16.04 or 14.04 (64 bit).

2. Anaconda package distributor and Python 3.6.5. 
A virtual environment with all the dependencies can be created from a environment.yml file contained in the repository.
	
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

1. Extracting sequences flanking a codon position from genome (-21[3 codon bases]+21).
2. Estimating the editable mutations based on base editors and mutations chosed.
3. Designing guides.
4. Checking offtarget effects.

## Usage

To list supported pams and editors

	beditor --list pams
	beditor --list editors

These lists are located in `beditor/data` folder and can be modified. 

To run all the analysis steps in tandem,

	beditor --cfg config.yml 

To run a single step,

	beditor --step {step number} --cfg config.yml 

Here, `config.yml` is a configuration file that contains all the input parameters needed for the analysis.

## Configuration

1. Make a configuration `yaml` file (see test.yml for example)

This file contains all the input parameters needed for the analysis:
	
	# shown in square brackets are defaults
	# input file path
	dinp: input.tsv

	#common crispr params
	pams: ['NGG','NG']

	#common 
	## cpus/threads [1]
	cores: 6
	## number of lines of input file to process per cpu [100]
	chunksize: 40

	# 01_sequences
	## host information
	host: scientific name
	# check release and assembly from http://useast.ensembl.org/index.html
	genomerelease: TakeFromFromEnsemblSite
	genomeassembly: TakeFromFromEnsemblSite

	# 02_mutations
	##N if nonsynonymous, S if syn, [no input if both]
	mutation_type: N
	## keep nonsense mutations [True]
	keep_mutation_nonsense: False
	## allowed nucleuotide substitutions per codon [1]
	max_subs_per_codon: 1
	## base editors to use (restriction max_subs_per_codon would override the choice of base editors)
	BEs: ['Target-AID','ABE']

	## Mutations information can be provided in 3 options: 
	## 1. Required Mutations mentioned in input file (in a column called "amino acid mutation") would override this 
	## 2. Required Substitutions provided as a file
	## 3. Carry out Mimetic substitutions (base on genome wide substitution maps). Only for human and yeast.
	## input: options 
	## mutations if option 1, substitutions if option 2, mimetic if option 3, [no input if keep all possible mutations (slow)]
	mutations: 

	## Option specific options
	## 2. Substitutions provided as a file [no input]
	dsubmap_preferred_path: 

	## 3. Mimetic substitutions
	## mimetism level (high if only the best one, [medium if best 5], low if best 10)
	mimetism_level: medium

	## can not mutate between these [no input]
	# non_intermutables: ['S','T','K']

	## 04offtargets [3]
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
If parallel processing is used, this folder would store individual parts (chunks) of the analysis. 

## Test datasets

	cd test_dataset
	cd {organism name}
	beditor --cfg project_name_all.yml

