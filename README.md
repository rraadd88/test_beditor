# `beditor`

Python package to design guides for CRISPR base editing. 

## Requirements

1. Ubuntu 16.04 and 14.04 (64 bit).

2. Python 3.6.5 and Anaconda package distributor. A virtual environment can be created from environment.yml file in the repo.

	conda env create -f environment.yml

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

	beditor config.yml 

To run a single step,

	beditor --step {step number} config.yml 

Here, `config.yml` is a configuration file that contains all the input parameters needed for the analysis.

## Configuration

1. Make a configuration `yaml` file (see test.yml for example)

This file contains all the input parameters needed for the analysis:

	# Input file path 
	## contains two (tab-separated) columns: ensembl 
	## 1. 'transcript: id' : ensembl id 
	## 2. 'aminoacid: position' : 1-based indexing
	dinp: din_human.tsv

	# Common
	## cpus/threads for parallel processing
	cores: 6
	## number of lines of of input file to process per core 
	chunksize: 100

	# Step-wise parameters

	## 1. Extracting sequences (-21[3 codon bases]+21) flanking a codon position, from genome.
	## host information
	host: homo_sapiens
	genomerelease: 92
	genomeassembly: GRCh38

	## 2. Estimating the editable mutations based on base editors choosed.
	## base editors to use
	BEs: ['Target-AID','ABE']
	## Type of mutation 
	## N : nonsynonymous (default) | S : synonymous | none : both
	mutation_type: N
	## Keep nonsense
	keep_mutation_nonsense: False
	## Allowed nucleotide substitutions per codon
	max_subs_per_codon: 1
	## Allow mimetic or preffered substitutions
	## M: mimetic (default) | P: preffered (need path below) | both: both | none : keep all
	submap_type: M
	## Mimetism level 
	## high: only the single best one | medium: best 5 (default) | low: best 10 
	mimetism_level: medium
	## Custom preferred substitutions (overrides mimetic one)
	## contains 3 tab-separated columns 
	## 1. amino acid : reference amino acid
	## 2. amino acid mutation : mutated amino acid
	## 3. substitute : True if substitute else False.  
	dsubmap_preferred_path:
	## Can not mutate between these
	## only applies to mimetic substitutions
	non_intermutables: ['S','T']

	## 3. Designing guides.
	## PAM sequence
	## full list of supported PAMs is located at ./beditor/data/dpam.tsv
	pam: ['NGG','NG'] 

	## 4. Checking offtarget effects.
	## Number of mismatches allowed for bwa alignment
	## higher is slower
	mismatches_max: 5

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

## Visualizations

1. Individual mutation

Shows all the possible ways a mutation can be carried out. Also creates a genebank file.

2. Cumulative #TODO
A distribution plot guides 
x axis nucleiotide position 
x counts of nucleiotides
shows guides on both the strands

in columns: type of pam used
in subrows: type of pam
in rows: position of editing

## Install new genomes

Open this file in text editor

	/home/{user}/anaconda/envs/beditor/lib/python3.6/site-packages/pyensembl/species.py

and append genome info in this format

	{speciesname} = Species.register(
	    latin_name="{}",
	    synonyms=["{}"],
	    reference_assemblies={
	        "{}": (76, MAX_ENSEMBL_RELEASE),
	    })

eg. 
	yeast = Species.register(
	    latin_name="saccharomyces_cerevisiae",
	    synonyms=["yeast"],
	    reference_assemblies={
	        "R64-1-1": (76, MAX_ENSEMBL_RELEASE),
	    })

#TODOs

- Data collation after parallel processing.
- Integrate visualizations.