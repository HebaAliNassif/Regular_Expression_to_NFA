"""
References:
    -   Converting Regular Expressions to Postfix Notation with the Shunting-Yard Algorithm: https://gregorycernera.medium.com/converting-regular-expressions-to-postfix-notation-with-the-shunting-yard-algorithm-63d22ea1cf88
"""
import re

operator_priority_map = {
    '|': 10,    #or
    '+': 10,    #union
    '.': 20,    #concatenation
    '*': 30     #zero or more
    }
    
def is_literal(a):
  return (operator_priority_map.get(a, 0) == 0 and a != '(' and a != ')')


def is_binary_operator(a):
  return (a == '|') or (a == '+');


def is_left_unary_operator(a):
  return (a == '(');
  
def validate_regex(regex, normal_regex):
    #Check using re
    try:
        re.compile(normal_regex)
    except re.error as e:
        print("Error:\n\tInvalid expression.\n\t"+ str(e).capitalize())
        exit(-1)
        
    #check '.' symbol
    if  len(normal_regex) > 0 and '.' in normal_regex:
        print("Error:\n\tInvalid expression.\n\tA regular expression cannont have a '.' symbol.")
        exit(-1)
        
    #check valid begining
    if  len(regex) > 0 and not is_left_unary_operator(regex[0]) and regex[0] != '[':                 
        if not(is_literal(regex[0])) or regex[0] == ']':
            print("Error:\n\tInvalid expression.\n\t'" +regex[0]+ "' cannot exist at the begining of a regular expression.")
            exit(-1)
            
    #check valid ending
    if  len(regex) > 0 and regex[-1] != ')' and regex[-1] != ']':                 
        if is_binary_operator(regex[-1]) or regex[-1] == '(' or regex[-1] == '[':
            print("Error:\n\tInvalid expression.\n\t'" +regex[-1]+ "' cannot exist at the end of a regular expression.")
            exit(-1)
    
    #check repeated operators
    for i in range(1, len(regex)):
        #check space
        if ' ' == regex[i]:
            print("Error:\n\tInvalid expression.\n\tA regular expression cannont have a space.")
            exit(-1)
            
        #check empty parentheses
        if regex[i-1] == '(' and regex[i] == ')':
            print("Error:\n\tInvalid expression.\n\t" + "Empty parentheses are invalid")
            exit(-1)
            
        #check repeated operators    
        if regex[i] != '(' and regex[i] != ')':
            if regex[i] == regex[i-1] and not(is_literal(regex[i])) and not(is_literal(regex[i-1])):
                print("Error:\n\tInvalid expression.\n\t'" +regex[i]+ "' cannot be repeated.")
                exit(-1)


def insert_concatenation_operators_regex(regex_string):
    j = 0
    i = 0
    regex = []
    temp = list(regex_string)
    regex.insert(0, temp[0])
    #insert concatenation operators
    while i < len(temp):
        if temp[i] == '[' or temp[i] == '\'' or temp[i] == '"':
            if i > 0 and i < len(temp) and (is_literal(temp[i]) or is_left_unary_operator(temp[i])):
                if (not(is_binary_operator(temp[i-1]) or is_left_unary_operator(temp[i-1]))):
                    if j < len(regex):
                        regex[j] = '.'
                    else:
                        regex.insert(j, '.')
                    j += 1
            my_string = []
            operator = temp[i]
            end_operator = ']' if temp[i] == "[" else temp[i]
            i += 1
            if temp[i] == operator:
                print("Error:\n\tInvalid expression.\n\t", operator,"is repeated.")
                exit(-1)
            while(i < len(temp) and temp[i] != end_operator):
                my_string.append(temp[i])
                i += 1
            if i!= 0 and i < len(temp) and temp[i] == end_operator:
                i += 1
                if j < len(regex):
                    regex[j] = "".join(my_string)
                else:
                    regex.insert(j, "".join(my_string))
                j += 1
                if i < len(temp) and (is_literal(temp[i]) or is_left_unary_operator(temp[i])):
                    if (not(is_binary_operator(temp[i-1]) or is_left_unary_operator(temp[i-1]))):
                        if j < len(regex):
                            regex[j] = '.'
                        else:
                            regex.insert(j, '.')
                        j += 1
            else:
                print("Error:\n\tInvalid expression.\n\t", end_operator,"is missing.")
                exit(-1)
        elif temp[i] == ']':
            print("Error:\n\tInvalid expression.\n\t","] is invalid.")
            exit(-1)
        elif i!= 0 and i < len(temp):
            if is_literal(temp[i]) or is_left_unary_operator(temp[i]):
                if (not(is_binary_operator(temp[i-1]) or is_left_unary_operator(temp[i-1]))):
                    if j < len(regex) and regex[j-1] != '.':
                        regex[j] = '.'
                        j += 1
                    elif j >= len(regex):
                        regex.insert(j, '.')
                        j += 1
            if j < len(regex):
                regex[j] = temp[i]
            else:
                regex.insert(j, temp[i])
            j += 1
            i += 1
                
        elif i== 0:
            j += 1
            i += 1
        
    return regex    
    
def shunt_regex(regex):
    queue = []
    stack = ""
    i = 0
    while i < len(regex):
        if regex[i] == '(':
            stack = stack + regex[i]
        elif regex[i] == ')':
            while len(stack) > 0 and stack[-1] != '(':
                queue.append(stack[-1]) 
                stack = stack[:-1]
            if len(stack) == 0:
                print("Error:\n\tInvalid expression.\n\tRight parentheses is missing '('.")
                exit(-1)
            stack = stack[:-1]
        elif regex[i] in operator_priority_map:
            while len(stack) > 0 and operator_priority_map.get(regex[i], 0) <= operator_priority_map.get(stack[-1], 0):
                if stack[-1] == '(':
                    print("Error:\n\tInvalid expression.\n\tLeft parentheses is missing ')'.")
                    exit(-1)
                queue.append(stack[-1])
                stack = stack[:-1]
            stack = stack + regex[i]
        else:
            queue.append(regex[i])
            
        i += 1
    while stack:
        if stack[-1] == '(':
            print("Error:\n\tInvalid expression.\n\tLeft parentheses is missing ')'.")
            exit(-1)
        queue.append(stack[-1])
        stack = stack[:-1]
        
    #check repeated operators
    for i in range(1, len(queue)):
        if queue[i] == queue[i-1] and not(is_literal(queue[i])) and not(is_literal(queue[i-1])):
            print("Error:\n\tInvalid expression.\n\t'" +queue[i]+ "' cannot be repeated.")
            exit(-1)    
    return queue