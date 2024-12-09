def read_grammar(file_path):
    grammar_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '~' in line:
                head, body = line.split('~')
                head = head.strip()
                derivations = [derivation.strip() for derivation in body.split('|')]
                if head not in grammar_dict:
                    grammar_dict[head] = []
                grammar_dict[head].extend(derivations)
    return grammar_dict


def display_grammar(grammar_dict):
    for non_terminal, derivations in grammar_dict.items():
        print(f"{non_terminal}: {derivations}")


if __name__ == "__main__":
    grammar_file = "grammar.txt"
    grammar_dict = read_grammar(grammar_file)
    display_grammar(grammar_dict)
