#     import subprocess
from beditor.lib.io_sys import runbashcmd
from os.path import exists
from glob import glob
from os.path import basename,dirname

def test_species(host='saccharomyces_cerevisiae',genomeassembly='R64-1-1'):
    import yaml 
    cfg=yaml.load(open('common/configuration.yml','r'))
    cfg['genomeassembly']=genomeassembly
    com=f"source activate beditor;python make_datasets.py --species {host} --genomerelease {cfg['genomerelease']} --genomeassembly {cfg['genomeassembly']}"
    runbashcmd(com,test=True)
    for datasetd in glob('dataset_*'):
        for cfgp in glob(f"{datasetd}/*.yml"):
            cfgp=basename(cfgp)
            com=f"source activate beditor;cd {datasetd};beditor --cfg {cfgp}"
            runbashcmd(com,test=True)

test_species()
