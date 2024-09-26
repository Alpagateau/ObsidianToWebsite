import os
import time

from parser.utils import *
from parser.lexer import *
from parser.parser import *
from parser.renderer import *

# folder path 
dir_path = './Revisions/Cours/'

# list to store files 
res = []

# Iterate directory 
for path in os.listdir(dir_path): 
    # check if current path is a file 
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

div = len(res)
err = 0
erl = []
start = time.time()
for i in range(div):
    #print(res[i])
    try:
        render(
            BuildTree(
                Lexer(
                    LoadFile(dir_path + res[i])
                )
            )
        )
    except:
        err +=1
        erl += [res[i]]
end = time.time() 
# ['Intégration discrète.md', 'Nombres quantiques.md', 'Oscillateur Harmonique.md']
#print("Total time :", (end - start), "| mean time : ", (end-start)/(div-err), "ERR : ", err)
#print(erl)

render(
    BuildTree(
        Lexer(
            LoadFile(dir_path + "Intégration discrète.md")
        )
    )
)
