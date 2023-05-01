#!/usr/bin/env python

import sys
import yaml
import string


def out(s, outfile=sys.stdout):
    outfile.write(s)

uniq = 1

def getID():
    global uniq
    n = str(uniq)
    uniq += 1
    return n

def asAttr(attr, val):
    escaped = val.replace('\"', '\\\"')  # " -> \"
    return " [" + attr + "=\"" + escaped + "\"]"

#def render(ast, num, name=None, outfile=None):
def render(ast, name=None, outfile=None):
    if name is None:
        name = getID()
        #num = str(int(num)+1)
        #name = num

    lab = ""
    edges = []  # (from, to, attr)

    if type(ast) is dict:
        for key,val in ast.items():

            if type(val) is dict:
                child = getID()
                #num = str(int(num)+1)
                #child = num
                edges.append((name, child, asAttr("label", key)))
                #render(val, child, num, outfile=outfile)
                render(val, child, outfile=outfile)

            elif type(val) is list:
                last = None
                for i in val:
                    child = getID()
                    #num = str(int(num)+1)
                    #child = num
                    #if int(child) < 3:
                    edges.append((name, child, asAttr("label", key)))
                    #render(i, child, num, outfile=outfile)
                    render(i, child, outfile=outfile)
                    if last is not None:
                        edges.append((last, child, asAttr("style", "dashed")))
                    last = child
                    #else:
                    #    lab += (str(key) + ": " + str(val) + "\\n")

            else:
                lab += (str(key) + ": " + str(val) + "\\n")

    else:
        lab += str(ast)

    # output vertex
    out(name + asAttr("label", lab) + ";\n", outfile=outfile)

    # output edges
    for (src, dest, attr) in edges:
        out(src + " -> " + dest + attr + ";\n", outfile=outfile)




######################
# "main"

# check args
# myself = sys.argv[0]
# if len(sys.argv) != 2:
#     print("error: invalid number of arguments.")
#     print("usage:\t" + myself + " [path to YAML file]")
#     sys.exit(1)

# infile = sys.argv[1]

# with open(infile, 'r') as stream:
#     try:
#         ast = yaml.safe_load(stream)

#         out ("digraph graphname {\n")

#         render(ast)

#         out ("}\n")

#     except yaml.YAMLError as exc:
#         print("pyYAML Parsing Error:")
#         print(exc)
#         sys.exit(1)

def gen_gv(playbook):

    name = playbook.split('/')[-1].split('.')[0]

    with open(playbook, 'r') as stream:
        ast = yaml.safe_load(stream)[0]

    with open('/data/minh/CompilierFuzzing/similarity/IR/vis/' + name + '.gv', 'w') as f:

        out('digraph graphname {\n', outfile=f)
        #num = str(0)
        #render(ast, num, outfile=f)
        render(ast, outfile=f)
        out('}\n', outfile=f)

    from graphviz import Source

    # Create a Graphviz source object from the DOT file
    graph = Source.from_file('/data/minh/CompilierFuzzing/similarity/IR/vis/' + name + '.gv')

    # Render the PDF file
    graph.render(filename='/data/minh/CompilierFuzzing/similarity/IR/vis/' + name, format='png', cleanup=True)

    return graph.source

if __name__ == '__main__':
    
    dir = '/data/minh/CompilierFuzzing/similarity/YAML/chatgpt_0.yaml'
    gen_gv(dir)

    print('done')

