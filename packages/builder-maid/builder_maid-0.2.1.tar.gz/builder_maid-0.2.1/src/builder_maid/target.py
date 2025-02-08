import subprocess
import os

class target:
    _compiler : str
    _flags : str
    _files : str
    _defines : list[str]
    _include_dirs : list[str]
    _lib_dirs : list[str]
    _libs : list[str]
    _cwd : str

    def __init__(self, compiler : str):
        self._compiler = compiler
        self._cwd = os.getcwd()

    def set_cwd(self, cwd):
        self._cwd = cwd;

    def set_compiler(self, compiler : str):
        self._compiler = compiler
    
    def add_files(self, files : str):
        if type(files) == str:
            self._files += ' ' + files
            return
        if type(files) == list[str]:
            for i in files:
                self._files += ' ' + files

    def add_flags(self, flags):
        if type(flags) == str:
            self._files += " -" + flags
            return
        if type(flags) == list[str]:
            for i in flags:
                self._files += " -" + flags

    def add_include_dir(self, dir : str):
        self._include_dirs.append(dir)
    
    def add_lib_dir(self, dir : str):
        self._lib_dirs.append(dir)

    def add_lib(self, path : str):
        self._libs.append(path)

    def add_define(self, define : str):
        self._defines.append(define)

    def compile(self, output : str):
        file_str = ""
        for i in self._files:
            file_str += i + ' '
        
        flags_str = ""
        for i in self._flags:
            flags_str += i + ' '

        subprocess.run(self.get_command(), shell=True, cwd=self._cwd)

    def get_command(self) -> str:
        cmd = f"{self._compiler} {self._files} {self._flags}"

        for i in self._include_dirs:
            cmd += f" -I{i}"
        for i in self._defines:
            cmd += f" -D{i}"
        for i in self._lib_dirs:
            cmd += f" -L{i}"
        for i in self._libs:
            cmd += f" -l{i}"
        
        return cmd;
