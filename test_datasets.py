#     import subprocess
from beditor.lib.io_sys import runbashcmd
from os.path import exists
from glob import glob
from os.path import basename,dirname

def test_species(host='saccharomyces_cerevisiae',genomeassembly='R64-1-1'):
    import yaml 
    cfg=yaml.load(open('common/configuration.yml','r'))
    # clone test_beditor 
    if not exists('test_beditor'):
        runbashcmd('git clone https://github.com/rraadd88/test_beditor.git',test=True)
    else:
        runbashcmd('cd test_beditor;git pull',test=True)
    cfg['genomeassembly']=genomeassembly
    com=f"source activate beditor;cd test_beditor;python make_datasets.py --species {host} --genomerelease {cfg['genomerelease']} --genomeassembly {cfg['genomeassembly']}"
    runbashcmd(com,test=True)
    for datasetd in glob('test_beditor/dataset_*'):
        for cfgp in glob(f"{datasetd}/*.yml"):
            cfgp=basename(cfgp)
            com=f"source activate beditor;cd {datasetd};beditor --cfg {cfgp}"
            runbashcmd(com,test=True)

test_species()
