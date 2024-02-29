import hashlib
import os
import shutil
from pathlib import Path


BLOCKSIZE = 65536

def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    
    return hasher.hexdigest()

def sync2(source, dest):
    # Walk the source folder and build a dict of filenames and their hashes
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder)/ fn)] = fn
    
    
    seen = set() # Keep track of the files we've found in the target
    
    # Walk the target folder and get the files we've found in the target
    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path : Path = Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)
            
            # if there's a file in target that's not in source, delete it
            if dest_hash not in source_hashes:
                dest_path.remove()
                
            # if there's a file in target that has a different path in source,
            # move it to the correct path
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder)/ source_hashes[dest_hash])
    
    # for every file that appears in source but not target, copy the file to the target
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source)/ fn, Path(dest)/ fn)
            

def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath
        
        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath
    
    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename
            
    
            