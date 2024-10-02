from parser.utils import *
from parser.lexer import *
from parser.parser import *

t = LoadFile("POC/test.md")
l = Lexer(t)
tree = BuildTree(l)
PrintTree(tree)
