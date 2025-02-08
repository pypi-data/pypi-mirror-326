import subprocess
import os

class target:
    _compiler : str
    _flags : list[str]
    _files : list[str]

    def __init__(self):
        self._compiler = ""
        self._files = []
        self._flags = []

    def set_compiler(self, cmp : str):
        self._compiler = cmp
    
    def add_files(self, files):
        self._files.append(files)

    def add_flags(self, flags):
        self._flags.append(flags)

    def compile(self, output : str):
        file_str = ""
        for i in self._files:
            file_str += i + ' '
        
        flags_str = ""
        for i in self._flags:
            flags_str += i + ' '

        subprocess.run(f"{self._compiler} {file_str} {flags_str} -o {output}", shell=True, cwd=os.getcwd())
