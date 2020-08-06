import os
import random

class colors:
    yellow =  '\033[1;33m'

def banner():
    logos_path = os.path.join(os.path.dirname(__file__), 'logos/')
    files = os.listdir(logos_path)
    index = random.randrange(0, len(files))
    f = open(os.path.join(f'{logos_path}', f'{files[index]}') , 'r')
    contents = f.read()
    print(colors.yellow + contents)
    f.close()
