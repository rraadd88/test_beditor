import yaml
import pyensembl
from os.path import dirname,basename
from os import makedirs

def make_test_dataset(cfgp,mutc=100):
#     cfgp='../test_beditor/worm/project_name_all.yml'
    with open(cfgp,'r') as f:
        cfg=yaml.load(f)
    import pyensembl
    cfg['host']=pyensembl.species.normalize_species_name(cfg['host'])        

    from beditor.lib.io_sys import runbashcmd

    runbashcmd(f"pyensembl install --reference-name {cfg['genomeassembly']} --release {cfg['genomerelease']} --species {cfg['host']}")

    import pyensembl
    ensembl = pyensembl.EnsemblRelease(species=pyensembl.species.Species.register(
                latin_name=cfg['host'],
                synonyms=[cfg['host']],
                reference_assemblies={
                    cfg['genomeassembly']: (cfg['genomerelease'], cfg['genomerelease']),
                }),release=cfg['genomerelease'])
    print([c for c in ensembl.contigs() if not '.' in c])

    # make test data

    import pandas as pd
    import numpy as np
    from os.path import dirname,splitext
    aas='ACDEFGHIKLMNPQRSTVWY*'
    mutations=np.repeat(list(aas), (mutc//len(aas))+1)
    dinput=pd.DataFrame(columns=['transcript: id','aminoacid: position','amino acid mutation'],
                       index=range(len(mutations)),
                       )
    i=0
    for t in ensembl.transcripts():
        if t.contig!='MITO':
            if t.is_protein_coding:
                if t.contains_start_codon and t.contains_stop_codon:
                    if not t.protein_sequence is None:
                        dinput.loc[i,'transcript: id']=t.id
                        dinput.loc[i,'aminoacid: position']=t.protein_sequence.find('K')+2
                        dinput.loc[i,'amino acid mutation']=mutations[i]
                        i+=1
        if i==len(mutations):
            break
        #                 break
    dinput=dinput.head(mutc)
    print(dinput.shape)

    dinput.to_csv(f"{dirname(cfgp)}/input.tsv",sep='\t')
               
def make_cfg(cfgp_template,host,genomerelease,genomeassembly,mutc=100):
    with open(cfgp_template,'r') as f:
        cfg=yaml.load(f)
    cfg['host']=host
    cfg['genomerelease']= genomerelease
    cfg['genomeassembly']= genomeassembly
    cfg['host']=pyensembl.species.normalize_species_name(cfg['host'])
               
    cfgp=f"{dirname(cfgp_template)}/../{cfg['host']}/{basename(cfgp_template)}"
    makedirs(dirname(cfgp),exist_ok=True)
    with open(cfgp, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False)                
    make_test_dataset(cfgp,mutc=mutc)        
    return cfgp
