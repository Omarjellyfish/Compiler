import re
from typing import List, Tuple

# Grammar terminal tokens
KEYWORDS = {'var', 'for', 'in', 'if', 'print', 'to'}
OPERATORS = {'+', '-', '*', '/', '%', '=', '==', '>=', '<=', '>', '<', '!='}
DELIMITERS = {'(', ')', ':', ';'}
WHITESPACE = {' ', '\n', '\t'}

# Token patterns
TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(var|for|in|if|print|to)\b'),        # Matches keywords
    ('NUMBER', r'\b\d+\b'),                              # Matches integers
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),       # Matches variable names or identifiers
    ('OPERATOR', r'==|>=|<=|!=|[+\-*/%=]'),              # Matches operators
    ('DELIMITER', r'[();:]'),                            # Matches delimiters
    ('STRING', r'".*?"'),                                # Matches double-quoted strings
    ('CHAR', r"'[a-zA-Z ]'"),                            # Matches single characters
    ('WHITESPACE', r'\s+'),                              # Matches any whitespace
    ('RANGE', r'\(\s*\d+\s*to\s*\d+\s*\)'),               # Matches range syntax (e.g. (1 to 10))
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)

def tokenize(code: str, line_number: int) -> List[Tuple[str, str, int]]:
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup
        value = match.group(kind)
        
        # Skip whitespace
        if kind == 'WHITESPACE':
            continue
        
        # Handle keywords and identifiers
        elif kind == 'IDENTIFIER' and value in KEYWORDS:
            kind = 'KEYWORD'
        
        # Handle 'for' loop detection
        elif kind == 'KEYWORD' and value == 'for':
            tokens.append(('KEYWORD', 'for', line_number))
            continue
        
        # Handle the range in for loops
        elif kind == 'RANGE':
            tokens.append(('RANGE', value, line_number))
            continue
        
        # Append the token (ignoring whitespace)
        tokens.append((kind, value, line_number))
    
    return tokens

def execute():
    all_tokens = []
    
    # Read the file and tokenize line by line
    with open('EvenOddProgramWithMiniLanguage.txt', 'r') as file:
        for line_number, line in enumerate(file, start=1):
            all_tokens.extend(tokenize(line, line_number))
    
    return all_tokens

def main():
    print("Tokens:")
    
    # Print each token from the executed tokenization process
    for token in execute():
        print(token)

if __name__ == "__main__":
    main()
