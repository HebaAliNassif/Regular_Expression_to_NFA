"""
References:
    -   Visualizing Thompson’s Construction Algorithm for NFAs, step-by-step: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b
"""
states_transitions = dict().copy()
start_states = set()
termination_states = set()
class state: 
    label = None
    edges = None
    def __init__(self, label):
        self.label = label
        self.edges = dict().copy()
        
class nfa:
    initial = None
    accept = None
    
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept
    
def compile(regex):
    stack = []
    state_number = 0
    for c in regex:
        if c == '+' or c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            
            initial = state("S" + str(state_number))
            state_number += 1
            
            accept = state("S" + str(state_number))
            state_number += 1
            
            start_states.remove(nfa1.initial.label) 
            termination_states.remove(nfa1.accept.label)
            
            start_states.remove(nfa2.initial.label) 
            termination_states.remove(nfa2.accept.label)
            
            start_states.add(initial.label)
            termination_states.add(accept.label)
            
            initial.edges["Epsilon1"] = nfa1.initial
            initial.edges["Epsilon2"] = nfa2.initial
            
            nfa1.accept.edges["Epsilon1"] = accept
            nfa2.accept.edges["Epsilon2"] = accept

            newNFA = nfa(initial, accept)
            stack.append(newNFA)
        elif c == '*':
            nfa1 = stack.pop() 
            
            initial = state("S" + str(state_number))
            state_number += 1
            
            accept = state("S" + str(state_number))
            state_number += 1
            
            initial.edges["Epsilon1"] = nfa1.initial
            initial.edges["Epsilon2"] = accept
            
            start_states.remove(nfa1.initial.label) 
            termination_states.remove(nfa1.accept.label)
            
            start_states.add(initial.label)
            termination_states.add(accept.label)

            nfa1.accept.edges["Epsilon1"] = initial
            nfa1.accept.edges["Epsilon2"] = accept

            newNFA = nfa(initial, accept)
            stack.append(newNFA)
        elif c == '.':
            nfa2 = stack.pop() 
            nfa1 = stack.pop()

            nfa1.accept.edges["Epsilon"] = nfa2.initial
            
            start_states.remove(nfa2.initial.label) 
            termination_states.remove(nfa1.accept.label)
            
            newNFA = nfa(nfa1.initial, nfa2.accept)
            stack.append(newNFA)
        else:
            initial = state("S" + str(state_number))
            state_number += 1
            
            accept = state("S" + str(state_number))
            state_number += 1            
            
            initial.edges[c] = accept 
            
            start_states.add(initial.label)
            termination_states.add(accept.label)
            
            newNFA = nfa(initial, accept)
            stack.append(newNFA)
    
    return stack.pop()
def DFSUtil(v, visited):

        if v.label not in visited:
            visited.add(v.label)
            new_list = list()
            states_transitions[v.label] = new_list
        for transiton, neighbour in v.edges.items():
            if(v.label in states_transitions.keys()):
                states_transitions[v.label].append((neighbour.label, transiton))
            else:
                new_list = list()
                new_list.append((neighbour.label, transiton))
                states_transitions[v.label] = new_list
            if neighbour.label not in visited:
                DFSUtil(neighbour, visited)
                
def DFS(nfa):
    visited = set()
    visited.add(nfa.initial.label)
    DFSUtil(nfa.initial, visited)