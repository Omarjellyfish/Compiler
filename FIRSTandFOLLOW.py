import transformationCode

grammar = transformationCode.read_grammar("grammar.txt")

def is_terminal(symbol):
    return symbol not in grammar.keys()

def calculate_first(grammar) :
    first = {}
    for non_terminal in grammar :
        first[non_terminal] = set()

    def first_of_symbol(symbol) :
        if symbol in grammar :
            return first[symbol]
        return {symbol}
    
    def first_for_rule(non_terminal , rule) :
        for symbol in rule.split() :
            symbol_first = first_of_symbol(symbol)
            first[non_terminal].update(symbol_first - {"ε"})
            if "ε" not in symbol_first :
                break
        else : 
            first[non_terminal].add("ε")
    
    updated = True
    while updated :
        updated = False
        for non_terminal , rules in grammar.items() :
            curr_size = len(first[non_terminal])
            for rule in rules :
                first_for_rule(non_terminal , rule)
            if len(first[non_terminal]) > curr_size :
                updated = True
    return first


first = calculate_first(grammar)

for non_terminal , first_set in first.items() :
    print(f"First({non_terminal}) = {first_set}")
    print()

follow = {}

def initialize_follow():
    for non_terminal in grammar:
        follow[non_terminal] = set()
    follow["<program>"].add("$")  

def get_follow(non_terminal):

    for lhs, productions in grammar.items():
        for production in productions:
            parts = production.split()

            for i, part in enumerate(parts):
        
                if part == non_terminal:  
                    for j in range(i + 1, len(parts)):
                        next_part = parts[j]
                        if is_terminal(next_part):
                            follow[part].add(next_part)
                            break
                        else:
                            follow[part].update(first[next_part])  

                            if "ε" in first[next_part]:
                                if lhs != part: 
                                    follow[part].remove({"ε"})
                                    follow[part].update(follow[lhs])  
                                break  
                        
                    else: 
                        follow[part].update(follow[lhs])

def compute_follow():
    initialize_follow()

    while True:
        updated = False
        for non_terminal in grammar:
            before_update = follow[non_terminal].copy()
            get_follow(non_terminal)
            if follow[non_terminal] != before_update:
                updated = True
        if not updated:
            break

compute_follow()

for non_terminal, follow_set in follow.items():
    print(f"Follow({non_terminal}) = {sorted(follow_set)}")
    print()
