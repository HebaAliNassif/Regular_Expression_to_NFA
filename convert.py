import plot
import regex_post_processing as regex_pp
import thompson
import create_JSON
import sys
import os

if (len(sys.argv) > 1):
    output_dir_name = sys.argv[1]
else:
    output_dir_name = "output"
try:
    if not os.path.exists(output_dir_name):
        os.makedirs(output_dir_name)
except:
    print("Invalid file name")
    exit(-1)
    
regex = input("Enter Regex: ")
concatenated_regex = regex_pp.insert_concatenation_operators_regex(regex)

regex_pp.validate_regex(concatenated_regex, regex)
print("Concatenated Regex:\t", "".join(concatenated_regex), "\t",concatenated_regex)

postfix_regex = regex_pp.shunt_regex(concatenated_regex)
print("Postfix Regex:     \t", "".join(postfix_regex), "\t",postfix_regex)

thompson.DFS(thompson.compile(postfix_regex))
print("Start States: ",thompson.start_states, "\nTermination States: ", thompson.termination_states)

plot.draw(thompson.states_transitions, thompson.start_states, thompson.termination_states, regex, output_dir_name)
create_JSON.formatJSON(thompson.states_transitions, thompson.start_states, thompson.termination_states, output_dir_name)