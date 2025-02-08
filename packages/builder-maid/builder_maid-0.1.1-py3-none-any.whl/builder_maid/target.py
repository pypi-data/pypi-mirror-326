import subprocess

class target:
    _compiler : str
    _flags : list[str]
    _files : list[str]

    def __init__():
        target._compiler = ""
        target._files = []
        target._flags = []

    def set_compiler(cmp : str):
        target._compiler = cmp
    
    def add_files(files):
        target._files.append(files)

    def add_flags(flags):
        target._flags.append(flags)

    def compile(output : str):
        file_str = ""
        for i in target._files:
            file_str += i + ' '
        
        flags_str = ""
        for i in target._flags:
            flags_str += i + ' '

        subprocess.run(f"{target._compiler} {file_str} {flags_str} -o {output}")
