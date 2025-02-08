import os
import re
import hashlib
from os import path
from glob import glob
AVAIL_FORMAT=["sto", "a3m"]

def recursive_msa_lookup(pattern:str):
    """ yield .sto or a3m files that match the pattern
        if pattern: 
            - is a directory, recursively look for all sto or a3m files
            - is a glob expression, with a3m or sto ending, use it directly
            - is glob expression without a a3m or sto ending, extend it for a3m and sto files
    """
    if path.isdir(pattern):
        for ext in AVAIL_FORMAT:
            for msa_file in glob(f"{pattern}/**/*.{ext}", recursive=True):
                yield msa_file
    else:
        maybe_ext = f_ext(pattern)
        if maybe_ext != '' and not maybe_ext in AVAIL_FORMAT:
            raise ValueError(f"{maybe_ext} is not a valid MSA format")
        if maybe_ext == '':
            for ext in AVAIL_FORMAT:
                ext = f'*.{ext}' if pattern[-1] != '*' else f'{pattern}.{ext}'
                for msa_file in glob(f"{pattern}.{ext}"):
                    yield msa_file
            return
        for msa_file in glob(pattern):
            yield msa_file
        
def f_ext(fpath):
    _, file_ext = os.path.splitext(fpath)
    return file_ext.replace('.', '')

def apply_blueprint(queries:list[str], bp:dict)-> tuple[ list[tuple[str, str, str]], bool ]:   
    requests = [ (q, db['target'], db['label']) for db in bp['ingredients'] for q in queries ]
    pdqt     = bp['pdqt'] if 'pdqt' in bp else False
    
    return requests, pdqt

def mfasta_convert(from_file, to_file):
    re_line = r'(^.*[\S])[\s]+([\S]+)$'
    
    fasta_str = ''
    header = None
    with open(from_file, 'r') as fp:
        for l in fp:
            m = re.match(re_line, l)
            if not m:
                raise ValueError(f"Output format error:\n{l}")
            fasta_str += f">{m.groups()[0]}\n{m.groups()[1]}\n"       
    with open(to_file, 'w') as fp:
        fp.write(fasta_str)

def guess_target_msa_format(msa_target_file:str):
    ext = f_ext(msa_target_file)
    if not ext in AVAIL_FORMAT:
        raise ValueError(f"Unknown MSA format: {ext}")
    return ext

def hash_file(fpath):
    return hashlib.md5(open(fpath,'rb').read()).hexdigest()