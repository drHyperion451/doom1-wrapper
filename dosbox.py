import sys
import subprocess
from pathlib import Path
from configparser import ConfigParser

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

if __name__ == '__main__':
    config_path = Path('./wrapper.ini')
    config = ConfigParser()
    open_or_generate(config_path)

    config.read(config_path)
    EXEC = config['DEFAULT']['exec']
    ARGS = config['DEFAULT']['args']
    skip_next = False

    new_args = [EXEC, ARGS]

    for arg in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if arg in ["-conf", "-exit", "--fullscreen"]:
            skip_next = True
            continue
        new_args.append(arg)


        subprocess.run(new_args)
