# https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
import os
import subprocess

import IPython


# obtain ipython
try:
    ipython = IPython.get_ipython()
except AttributeError:
    try:
        import IPython.core.ipapi
        ipython = IPython.core.ipapi.get()
    except ModuleNotFoundError:
        import IPython.ipapi
        ipython = IPython.ipapi.get()


def write_file(filename, code):
    """
    Write a new file
    To make C/C++ source code file
    """
    ipython.run_cell_magic("writefile", filename, code)


def build_cpp(filename):
    """
    Build cpp file
    filename : ex) test or test.cpp
    """
    # Detect OS type because OSX may need different options
    # https://stackoverflow.com/questions/3466166/how-to-check-if-running-in-cygwin-mac-or-linux/18790824
    
    basename, ext = os.path.splitext(filename)
    if not ext:
        filename += '.cpp'

    ipython.run_cell_magic(
            "bash", "", ""
            # detect system type
            'unameOut="$(uname -s)"\n'
            'case "${unameOut}" in\n'
            '   Linux*)     machine=Linux;;\n'
            '   Darwin*)    machine=Mac;;\n'
            '   CYGWIN*)    machine=Cygwin;;\n'
            '   MINGW*)     machine=MinGw;;\n'
            '   *)          machine="UNKNOWN:${unameOut}"\n'
            'esac\n'
            # build command for system type
            'if [ $machine == "Linux" ]; then\n'
                 # build command for Linux
            f'    g++ -Wall -g -std=c++14 {filename} -o ./{basename} -Wa,-adhln={basename}.s\n'
            'elif [ "Mac" == $machine ]; then\n'
                 # build command for OSX
                 # https://stackoverflow.com/questions/10990018/
            f'    clang++ -S -mllvm --x86-asm-syntax=intel {filename}\n'
            f'    clang++ -Wall -g -std=c++14 {filename} -o ./{basename}\n'
            'else\n'
                 # Otherwise
            f'    g++ -Wall -g -std=c++14 {filename} -o ./{basename}.s -S\n'
            f'    g++ -Wall -g -std=c++14 {filename} -o ./{basename}\n'
            'fi\n'
    )


def run(cpp_filename):
    """
    Build cpp file
    cpp_filename : ex) test or test.cpp
    """
    basename, ext = os.path.splitext(cpp_filename)
    # https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
    # https://stackoverflow.com/questions/35160256/how-do-i-output-lists-as-a-table-in-jupyter-notebook

    # Run executable while capturing output
    result = subprocess.run([os.path.join(os.curdir, basename)], stdout=subprocess.PIPE)
    # present output
    print(result.stdout.decode())


def cleanup(cpp_filename):
    """
    Build cpp file
    cpp_filename : ex) test or test.cpp
    """
    basename, ext = os.path.splitext(cpp_filename)
    if not ext:
        cpp_filename += '.cpp'

    # to delete execution file
    if os.path.exists(basename):
        os.remove(basename)
    else:
        print(f"Unable to find {basename}")
        print(os.listdir())

    # to delete source file
    os.remove(cpp_filename)
