from __future__ import annotations
from textwrap import wrap
from ..utils import guess_target_msa_format, AVAIL_FORMAT, f_ext
from ..utils import recursive_msa_lookup
from glob import glob
import logging
from Bio import SeqIO, SeqRecord 

from os.path import basename
logger = logging.getLogger('msafLogger')
warner = logging.getLogger('msafWarnings')
from rich.text import Text
from rich.table import Table
from rich.console import Console
from rich import print
from ..utils import guess_target_msa_format
def factory(*args, dry=False, gap_in_cmp=False, nr=True):
    """
    Glob for MSA files and merge them into a single MSA
    """
    table = Table(title = "Merged MSAs" if not dry else "Available MSAs for merging")
    table.add_column("File", justify="left")
    table.add_column("Sequence counts", justify="right")
    table.add_column("Redundancy reject counts", justify="right")

    host_msa = ConcreteMSA()
    logger.debug(f"Attempting to merge: {args}")
    for _ in args:        
        logger.info(f"Processing {_}")
        for msa_file in recursive_msa_lookup(_):
            logger.debug(f"Loading {msa_file}")
            msa = ConcreteMSA(msa_file)           
            table.add_row( basename(msa_file), str(len(msa)), '[red]' + str(msa._nr_reject_counts) + '[/red]')
            if not dry:
                host_msa = ConcreteMSA.merge(host_msa, msa, gap_in_cmp, nr)
            #overlap = 
    if not dry:
        table.add_row( Text("Final MSA", style="bold"), str(len(host_msa)), f"[red bold]{host_msa._nr_reject_counts}[/red bold]") 
    console = Console()
    console.print(table)

    return host_msa

class ConcreteMSA:
    available_formats = AVAIL_FORMAT
    
    @staticmethod
    def merge(msa1:ConcreteMSA, msa2:ConcreteMSA, gap_in_cmp=False, nr=True):
        """
        Concatenate two msas, eventually applying non redundance check
        combined with accounting for gap or not to detect sequence identity/redundance
        """
        new_msa = ConcreteMSA(nr=nr, gap_in_cmp=gap_in_cmp)
       
        if msa1.query is None and msa2.query is None:
            logger.warn("Merging MSAs with no query")
            return new_msa
        if msa1.query is None:
            new_msa.push(msa2.query)
        elif msa2.query is None:
            new_msa.push(msa1.query)
        else:
            if msa1.query_seq != msa2.query_seq:
                raise ValueError("Query sequences don't match")
            new_msa.push(msa1.query)

        for _ in [msa1, msa2]:
            for r in _:
                b = new_msa.push(r)
                
        return new_msa        
    
    @classmethod
    def guess_format(cls, filename:str):
        if not f_ext(filename) in cls.available_formats:
            raise ValueError(f"{filename} doesn't have a valid MSA format")
        if f_ext(filename) == 'sto':
            return 'stockholm'
        return "fasta"

    def __init__(self, filename:str=None, nr=True, gap_in_cmp=False):
        self.nr = nr
        self.gap_in_cmp = gap_in_cmp
        self.query = None
        self._nr_reject_counts = 0
        self.registred_symbol = set()           
        self.in_records = []

        if filename:
            if not guess_target_msa_format(filename) in AVAIL_FORMAT:
                raise ValueError(f"Unknown MSA format: {filename}")
            for r in SeqIO.parse(filename, ConcreteMSA.guess_format(filename)):
                self.push(r)
                

    def __iter__(self)->SeqRecord:
        for r in self.in_records:          
            yield(r)
    @property
    def query_seq(self)->SeqRecord:
        return self.query.seq if self.gap_in_cmp else self.query.seq.replace('-', '') 

    def push(self, r:SeqRecord)->bool:
              
        if self.nr:
            if self.contains(r):
                warner.warn(
                    f"Redundant following input record:\n{viewifySeqRecord(r)}\n")
                #for _ in self.get_by_sequence(str(r.seq), self.gap_in_cmp):
                #    logger.warn(f"[Previous]{viewifySeqRecord(_)}")
                self._nr_reject_counts += 1
                return False
       
        r_as_seq = str(r.seq) if self.gap_in_cmp else str(r.seq).replace('-', '')     
        self.registred_symbol.add( r_as_seq ) 

        if self.query is None:
            self.query = r
        else:    
            self.in_records.append(r)
        
        return True
        
    def contains(self, r:SeqRecord):        
        r_seq = str(r.seq) if self.gap_in_cmp else  str(r.seq).replace('-', '') 
        if r_seq in self.registred_symbol:
            #print("FOUND " + r_seq + ' IN ' + str(self.registred_symbol))
            #exit(1)
            return True
        return False
    
    def __len__(self):
        return len(self.in_records) if self.query is None else len(self.in_records) + 1

    def get_by_sequence(self, seq:str, gap_in_cmp = False):
        """
        Costly function that will yield all msa entries that match provided sequence
        """
        
        if self.query.seq == seq:
            yield self.query

        for r in self.in_records:
            r_seq = str(r.seq) if gap_in_cmp else  str(r.seq).replace('-', '') 
            if r_seq == seq:
                yield r
    ## dump                 
        #in_records = SeqIO.parse(msa_file, "fasta")   
        #if fmt == 'sto':     
        #    output = os.path.join(cwd, 'results.sto')
        #    with open(output, "w") as fp:
        #       SeqIO.write(in_records, fp, "stockholm")    
    def write(self, filename):
        """
        Write MSA to desired file, supported foramts are .a3m and .sto
        """
        if self.query is None:
            raise ValueError("MSA has no query")
        ext = guess_target_msa_format(filename)
        fmt = 'stockholm' if ext == 'sto' else 'fasta'

        with open(filename, "w") as fp:
            fp.write( self.query.format(fmt) )
            for r in self.in_records:
                fp.write( r.format(fmt) )  
        logger.info(f"MSA written to {filename}")
    


def viewifySeqRecord(r:SeqRecord):
    #print(r)
    #print("0000")
    _ =  r.format("fasta")
    #print(_)
    #print("#")
    header = _.split('\n')[0]
    seq = str(r.seq).replace('-', '')
    seq = '\n'.join(wrap(seq, 80))
    #print(header)
    #print("##")    
    #print(seq)
    #print("###")    
    #exit(0)
    return f"{header}\n{seq}"

    #r(_)
    #exit(1)
    #return f"{header}\n{ wrap(seq, 80)}"
