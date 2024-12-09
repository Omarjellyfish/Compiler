import transformationCode
import tokenizer
from ParseTree import ParseTreeNode

grammar = transformationCode.read_grammar("grammar.txt")
tokensComp = tokenizer.execute()
tokens = [i[1] for i in tokensComp]

print("Grammar: ")
print(grammar)
print("Tokens: ")
print(tokens)
