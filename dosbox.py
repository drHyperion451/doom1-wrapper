import sys
import subprocess
from pathlib import Path
from configparser import ConfigParser

from shlex import split as shlex_split

def open_or_generate(config_path):
    if config_path.is_file() == False:
        config = ConfigParser()
        config['DEFAULT'] = {
            'exec': './dsda-doom.exe',
            'args': ''
        }
        with open(config_path, 'w') as config_file:
            config.write(config_file)
    pass

def game(sourcePort:str, iwad:str, extraPwads:str | None = None) -> str:

    cmdString = f"{sourcePort} -iwad {iwad}"
    if extraPwads != None:
        cmdString += f" -file {extraPwads}"

    cmdString += f' {ARGS}'
    # Splits into arguments. Just because subprocess.run needs this.
    cmdList = shlex_split(cmdString)


    completed_process = subprocess.run(cmdList, capture_output=True, text=True)
    
    # This will handle properly if errors had happened or not.
    O_STDERR = completed_process.stderr
    O_STDOUT = completed_process.stdout
    print(O_STDERR, O_STDOUT)

if __name__ == '__main__':
    config_path = Path('./wrapper.ini')
    config = ConfigParser()
    open_or_generate(config_path)

    config.read(config_path)
    EXEC = config['DEFAULT']['exec']
    ARGS = config['DEFAULT']['args']
    skip_next = False
    debug = False
    new_args = []

    for arg in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if arg in ["-conf", "-exit", "--fullscreen"]:
            skip_next = True
            continue
        if arg in ["--debugwrapper"]:
            skip_next = True
            debug = True
            continue
        new_args.append(arg)

        game(EXEC, ARGS)
        if debug: input()