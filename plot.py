from graphviz import Source
def readDictionary(dictionaery, start_states, termination_states, regex, output_dir_name):
    string = '''digraph G{
                fontsize=30
                rankdir=LR
                edge [dir=forward]
                '''
    string += ('label="'+regex.replace('"', "'")+'"\n')
    for parent, childs in dictionaery.items():
        if parent not in string:
            if parent in termination_states:
                string += (parent[1:] + ' [label="' + parent+'", shape=doublecircle]'+'\n')
            elif parent in start_states:
                string += (parent[1:] + ' [label="' + parent+'", shape=circle]' + '\n')
                string += ('start [label=start, shape=none] ' + '\n')
                string += ('start ->' + parent[1:] + '\n')
            else:
                string += (parent[1:] + ' [label="' + parent+'", shape=circle]' + '\n')
        for child, transiton in childs:
            if child not in string:
                if child in termination_states:
                    string += (child[1:] + ' [label="' + child+'", shape=doublecircle]'+'\n')
                else:
                    string += (child[1:] + ' [label="' + child+'", shape=circle]' + '\n')
            if 'Epsilon' not in transiton:
                string += (parent[1:] + '->' + child[1:]+ '[label="' + transiton + '"]'+ '\n')
            else:
                string += (parent[1:] + '->' + child[1:]+ '[label=ε]'+ '\n')
    string += '}'
    return string

def draw(dictionaery, start_states, termination_states, regex, output_dir_name):
    graph = readDictionary(dictionaery, start_states, termination_states, regex, output_dir_name)
    s = Source(graph, filename=output_dir_name +'/nfa.gv', format='png')
    s.view()