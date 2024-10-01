from parser.utils import *
from parser.lexer import *
from parser.parser import *

t = LoadFile("Revisions/Cours/variables et opérations.md")
l = Lexer(t)
tree = BuildTree(l)
PrintTree(tree)
