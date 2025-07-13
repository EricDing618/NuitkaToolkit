import ast,pprint

def test_ast():
    code = '''
import os
os.system("echo hello world")
    '''
    tree = ast.parse(code)
    pprint.pprint(ast.dump(tree))
test_ast()