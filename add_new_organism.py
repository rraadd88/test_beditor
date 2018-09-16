import yaml
import pyensembl
import pandas as pd
import numpy as np
from os.path import dirname,basename,splitext,abspath
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

    # # make test data

    # import pandas as pd
    # import numpy as np
    # from os.path import dirname,splitext
    # print([c for c in ensembl.contigs() if not '.' in c])

    # make test data

    aas='ACDEFGHIKLMNPQRSTVWY*'
    mutations=np.repeat(list(aas), (mutc//len(aas))+1)[:mutc]
    dinput=pd.DataFrame(columns=['transcript: id','aminoacid: position','amino acid mutation'],
                       index=range(len(mutations)),
                       )
    nts='ATGC'
    mutations_nucleotides=np.repeat(list(nts), (mutc//len(nts))+1)[:mutc]

    dinput_nucleotides=pd.DataFrame(columns=['genome coordinate','nucleotide mutation'],
                       index=range(len(mutations_nucleotides)),
                       )
    i=0
    for t in ensembl.transcripts():
        if t.contig!='MITO':
            if t.is_protein_coding:
                if t.contains_start_codon and t.contains_stop_codon:
                    if not t.protein_sequence is None:
                        #aminoacid
                        dinput.loc[i,'transcript: id']=t.id
                        dinput.loc[i,'aminoacid: position']=t.protein_sequence.find('K')+2
                        dinput.loc[i,'amino acid mutation']=mutations[i]
                        #nucleotide
                        loc=ensembl.locus_of_transcript_id(t.id).to_dict()
                        dinput_nucleotides.loc[i,'genome coordinate']=f"{loc['contig']}:{loc['start']-100}-{loc['start']-100}{loc['strand']}"
                        dinput_nucleotides.loc[i,'nucleotide mutation']=mutations_nucleotides[i]
                        i+=1
        if i==len(mutations):
            break       #                 break
    dinput=dinput.head(mutc)
    dinput_nucleotides=dinput_nucleotides.head(mutc)
    print(dinput.shape)

    dinput.to_csv(f"{dirname(cfgp)}/input_aminoacid.tsv",sep='\t')
    dinput_nucleotides.to_csv(f"{dirname(cfgp)}/input_nucleotide.tsv",sep='\t')
               
def make_cfg(cfgp_template,host,genomerelease,genomeassembly,mutc=100):
    with open(cfgp_template,'r') as f:
        cfg=yaml.load(f)
    cfg['host']=host
    cfg['genomerelease']= genomerelease
    cfg['genomeassembly']= genomeassembly
    cfg['host']=pyensembl.species.normalize_species_name(cfg['host'])
         
    print(f"cd {dirname(cfgp_template)}/../{cfg['host']}")
    print("source activate beditor")
    reverse_mutations=[True,False]
    mutation_formats=['aminoacid','nucleotide']
    mutations=['mutations','substitutions','mimetic',None]
    for mutation_format in mutation_formats:
        for mutation in mutations:
            if mutation=='mutations':
                for reverse_mutation in reverse_mutations:
                    direction='rev' if reverse_mutation else 'for'
                    cfgp=f"{dirname(cfgp_template)}/../{cfg['host']}/mutation_format_{mutation_format}_mutation_{mutation}_{direction}.yml"
                    makedirs(dirname(cfgp),exist_ok=True)
                    cfg['dinp']=f'input_{mutation_format}.tsv'
                    cfg['mutation_format']=mutation_format
                    cfg['mutations']=mutation            
                    cfg['reverse_mutations']=reverse_mutation            
                    with open(cfgp, 'w') as f:
                        yaml.dump(cfg, f, default_flow_style=False)                
                    print(f"beditor --cfg {basename(cfgp)}")
            else:
                if mutation=='substitutions':
                    cfg['dsubmap_preferred_path']=abspath('common/dsubmap.tsv')
                
                direction='for'
                cfgp=f"{dirname(cfgp_template)}/../{cfg['host']}/mutation_format_{mutation_format}_mutation_{mutation}_{direction}.yml"
                makedirs(dirname(cfgp),exist_ok=True)
                cfg['dinp']=f'input_{mutation_format}.tsv'
                cfg['mutation_format']=mutation_format
                cfg['mutations']=mutation            
                cfg['reverse_mutations']=reverse_mutation            
                with open(cfgp, 'w') as f:
                    yaml.dump(cfg, f, default_flow_style=False)                
                print(f"beditor --cfg {basename(cfgp)}")
    make_test_dataset(cfgp,mutc=mutc)        
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        