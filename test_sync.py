import tempfile
from pathlib import Path
import shutil
from sync import sync2, determine_actions


# def test_when_a_file_exists_in_the_source_but_not_the_destination():
#     source_hashes = {"hash1": "fn1"}
#     dest_hashes = {}
#     actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
#     assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]
    

# def test_when_a_file_has_been_renamed_in_the_source():
#     source_hashes = {"hash1": "fn1"}
#     dest_hashes = {"hash1": "fn2"}
#     actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
#     assert list(actions) == [("MOVE", Path("/src/fn2"), Path("/dst/fn1"))]
    
    
            
            
class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(("COPY", src, dest))
    
    def move(self, src, dest):
        self.append(("MOVE", src, dest))
    
    def delete(self, src, dest):
        self.append(("DELETE", src, dest))