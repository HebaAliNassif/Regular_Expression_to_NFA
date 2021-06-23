import json
def formatJSON(dictionary, start_states, termination_states, output_dir_name):
    output_dictionary = dict()
    output_dictionary["startingState"] = start_states.pop()
    i = 0
    for node, childs in dictionary.items():
        inner_dictionary = dict()
        if node in termination_states:
            inner_dictionary["isTerminatingState"] =  True
        else:
            inner_dictionary["isTerminatingState"] =  False
        for child, transiton in childs:
            if "Epsilon" not in transiton:
                if child not in inner_dictionary.keys():
                    inner_dictionary[transiton] = list()
                inner_dictionary[transiton].append(child)
            else:
                if "Epsilon" not in inner_dictionary.keys():
                    inner_dictionary["Epsilon"] = list()
                inner_dictionary["Epsilon"].append(child)
        output_dictionary[node] = inner_dictionary
        
    json_object = json.dumps(output_dictionary, indent = 4)
  
    with open(output_dir_name+"/nfa.json", "w") as outfile:
        outfile.write(json_object)
        
