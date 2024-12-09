from typing import List, Union

class ParseTreeNode:
    def __init__(self, symbol: str, value: Union[str, None] = None):
        self.symbol = symbol
        self.value = value
        self.children: List["ParseTreeNode"] = []

    def __str__(self):
        return f"{self.symbol} -> {self.value if self.value else 'No Value'}"
    
    def __repr__(self):
        # Improved __repr__ to show children too
        children_str = ', '.join([repr(child) for child in self.children])
        return f"ParseTreeNode(symbol={self.symbol}, value={self.value}, children=[{children_str}])"

    def add_child(self, child: "ParseTreeNode"):
        self.children.append(child)

    def traverse_dfs(self, level=0):
        indent = "  " * level
        print(f"{indent}Node: {self.symbol}, Value: {self.value}")
        for child in self.children:
            if child is not None:  # Ensure the child is not None
                child.traverse_dfs(level + 1)

def parse_logic_expr(expr):
    expr_parts = expr.split()
    if len(expr_parts) == 3:
        term1, comparison_op, term2 = expr_parts
        logic_expr_node = ParseTreeNode("<log-expr>", "Logic Expression")

        comparison_node = ParseTreeNode("<comparison>", "Comparison")
        comparison_node.add_child(ParseTreeNode(term1, term1))  # Assign the term1 value
        comparison_node.add_child(ParseTreeNode(comparison_op, comparison_op))  # Assign operator value
        comparison_node.add_child(ParseTreeNode(term2, term2))  # Assign the term2 value

        logic_expr_node.add_child(comparison_node)
        return logic_expr_node
    return None

def parse_assignment(statement):
    if '=' not in statement:
        return None  

    var_part, expr_part = statement.split('=')
    var_part = var_part.strip()
    expr_part = expr_part.strip()

    assignment_node = ParseTreeNode("<assignment>", "Assignment")

    var_node = ParseTreeNode("<var>", "Variable")
    identifier_node = ParseTreeNode("<identifier>", var_part)  # Assign the value here
    var_node.add_child(identifier_node)

    expr_node = ParseTreeNode("<expr>", "Expression")
    term_node = ParseTreeNode("<term>", "Term")

    if expr_part.isdigit():
        const_node = ParseTreeNode("<const>", expr_part)  # Assign value to constant
        term_node.add_child(const_node)
    else:
        term_node.add_child(ParseTreeNode("<var>", expr_part.strip()))  # Assign value to variable

    expr_node.add_child(term_node)

    assignment_node.add_child(var_node)
    assignment_node.add_child(ParseTreeNode("=", "="))  # Assign the '=' symbol value
    assignment_node.add_child(expr_node)

    return assignment_node

def parse_if_statement(statement):
    if_parts = statement.split("else")
    if_part = if_parts[0].strip()
    else_part = if_parts[1].strip() if len(if_parts) > 1 else None

    # Split condition and statement part
    if_condition_part, stmt_part = if_part.split(":")
    logic_expr_node = parse_logic_expr(if_condition_part.replace("if", "").strip())
    stmt_node = parse_assignment(stmt_part.strip())

    if_node = ParseTreeNode("<if-stmt>", "If Statement")
    if_node.add_child(logic_expr_node)
    if_node.add_child(ParseTreeNode(":", ":"))
    if_node.add_child(stmt_node)

    if else_part:
        else_stmt_node = parse_assignment(else_part.strip())
        else_node = ParseTreeNode("<else-stmt>", "Else Statement")
        else_node.add_child(else_stmt_node)
        if_node.add_child(else_node)

    return if_node

def parse_for_loop(statement, block_statements):
    # Split the statement by the colon (:) to separate the for loop definition and the block
    try:
        for_part, range_part = statement.split(":")
    except ValueError:
        raise ValueError(f"Invalid for loop syntax (missing colon): {statement}")
    
    # Clean up the loop part (remove 'for' and 'in')
    for_part = for_part.replace("for", "").replace("in", "").strip()

    # Now extract the loop variable and range part
    try:
        parts = for_part.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid for loop syntax: {statement}")

        loop_var = parts[1]
        range_expr = parts[2] if len(parts) > 1 else ""
    except ValueError:
        raise ValueError(f"Invalid for loop variable or range syntax: {statement}")

    # Handle the range expression in the format '( 0 to 10 )'
    range_expr = range_expr.replace("(", "").replace(")", "").strip()

    range_parts = range_expr.split("to")
    if len(range_parts) != 2:
        raise ValueError(f"Invalid range syntax in for loop: {statement}")
    
    start_range, end_range = range_parts[0].strip(), range_parts[1].strip()

    for_node = ParseTreeNode("<for-loop>", "For Loop")

    loop_var_node = ParseTreeNode("<loop-var>", "Loop Variable")
    loop_var_node.add_child(ParseTreeNode(loop_var, loop_var))  # Assign loop variable value

    range_node = ParseTreeNode("<range>", "Range")
    range_node.add_child(ParseTreeNode(f"start: {start_range}", f"start: {start_range}"))
    range_node.add_child(ParseTreeNode(f"end: {end_range}", f"end: {end_range}"))

    for_node.add_child(loop_var_node)
    for_node.add_child(ParseTreeNode("in", "in"))
    for_node.add_child(range_node)

    block_node = ParseTreeNode("<block>", "Block")
    for statement in block_statements:
        block_node.add_child(parse_assignment(statement.strip()))

    for_node.add_child(block_node)
    return for_node

def parse_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    statements = [line.strip() for line in lines if line.strip()]
    parse_tree_nodes = []

    block_statements = []

    for stmt in statements:
        if stmt.startswith("if "):
            parse_tree_nodes.append(parse_if_statement(stmt))
        elif stmt.startswith("for "):
            block_statements = ["result = result + i"]  # Extend this for dynamic block parsing
            parse_tree_nodes.append(parse_for_loop(stmt, block_statements))
        else:
            assignment_node = parse_assignment(stmt)
            if assignment_node:
                parse_tree_nodes.append(assignment_node)

    return parse_tree_nodes

# Example file path, you can adjust this path as per your file.
file_path = "EvenOddProgramWithMiniLanguage.txt"
parse_trees = parse_from_file(file_path)

# Print the parse trees with more detailed output
print("Parse Tree:")
for tree in parse_trees:
    tree.traverse_dfs()
