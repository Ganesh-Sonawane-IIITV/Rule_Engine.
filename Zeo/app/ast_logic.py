import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def is_operator(self):
        return self.type == "operator"

    def is_operand(self):
        return self.type == "operand"

    def evaluate(self, data):
        if self.is_operand():
            attribute, operator, target_value = self.value
            if attribute in data:  # Check if attribute exists in data
                return self._evaluate_condition(data[attribute], operator, target_value)
            return False  # Return False if attribute is missing in data

        if self.is_operator():
            if self.value == "AND":
                return self.left.evaluate(data) and self.right.evaluate(data)
            elif self.value == "OR":
                return self.left.evaluate(data) or self.right.evaluate(data)

        return False

    def _evaluate_condition(self, attribute_value, operator, target_value):
        # Normalize string comparisons
        if isinstance(attribute_value, str) and isinstance(target_value, str):
            attribute_value = attribute_value.lower()
            target_value = target_value.lower()

        if isinstance(attribute_value, type(target_value)):
            if operator == "==":
                return attribute_value == target_value
            elif operator == ">":
                return attribute_value > target_value
            elif operator == "<":
                return attribute_value < target_value
            elif operator == ">=":
                return attribute_value >= target_value
            elif operator == "<=":
                return attribute_value <= target_value
            elif operator == "!=":
                return attribute_value != target_value
        return False


def tokenize(rule_string):
    """
    Tokenizes the rule string into individual components (operators, operands, parentheses).
    """
    token_pattern = r"(\(|\)|AND|OR|[a-zA-Z_]+|[<>=!]+|'[^']*'|\d+)"
    tokens = re.findall(token_pattern, rule_string)
    return [t.strip() for t in tokens if t.strip()]


# def parse_condition(token):
#     """
#     Parses a condition token into an operand Node.
#     """
#     condition_pattern = r"([a-zA-Z_]+)\s*([<>=!]+)\s*'?(.*?)'?$"
#     match = re.match(condition_pattern, token)

#     if match:
#         attribute, operator, value = match.groups()

#         # Convert numeric values from string to integers
#         try:
#             value = int(value)
#         except ValueError:
#             pass  # Leave as string if not a number

#         return Node('operand', value=(attribute, operator, value))
#     else:
#         raise ValueError(f"Invalid condition token: {token}")

# Error Handling and Validation
def parse_condition(token):
    condition_pattern = r"([a-zA-Z_]+)\s*([<>=!]+)\s*'?(.*?)'?$"
    match = re.match(condition_pattern, token)

    if match:
        attribute, operator, value = match.groups()

        try:
            value = int(value)
        except ValueError:
            pass  # Leave as string if not a number

        return Node('operand', value=(attribute, operator, value))
    else:
        raise ValueError(f"Invalid condition token: '{token}' does not match expected pattern")




# def parse_tokens(tokens):
#     """
#     Parses the list of tokens recursively and builds an AST using Node objects.
#     """
#     def parse_expression(index):
#         left, index = parse_term(index)

#         while index < len(tokens) and tokens[index] == 'OR':
#             operator = tokens[index]
#             index += 1
#             right, index = parse_term(index)
#             left = Node('operator', left=left, right=right, value=operator)

#         return left, index

#     def parse_term(index):
#         left, index = parse_factor(index)

#         while index < len(tokens) and tokens[index] == 'AND':
#             operator = tokens[index]
#             index += 1
#             right, index = parse_factor(index)
#             left = Node('operator', left=left, right=right, value=operator)

#         return left, index

#     def parse_factor(index):
#         token = tokens[index]

#         if token == '(':
#             index += 1  # Skip '('
#             node, index = parse_expression(index)
#             index += 1  # Skip ')'
#             return node, index
#         else:
#             node = parse_condition(" ".join(tokens[index:index+3]))  # 3 tokens per condition
#             return node, index + 3

#     root, _ = parse_expression(0)
#     return root

# Error Handling and Validations
def parse_tokens(tokens):
    """
    Parses the list of tokens recursively and builds an AST using Node objects.
    """
    try:
        def parse_expression(index):
            left, index = parse_term(index)

            while index < len(tokens) and tokens[index] == 'OR':
                operator = tokens[index]
                index += 1
                right, index = parse_term(index)
                left = Node('operator', left=left, right=right, value=operator)

            return left, index

        def parse_term(index):
            left, index = parse_factor(index)

            while index < len(tokens) and tokens[index] == 'AND':
                operator = tokens[index]
                index += 1
                right, index = parse_factor(index)
                left = Node('operator', left=left, right=right, value=operator)

            return left, index

        def parse_factor(index):
            token = tokens[index]

            if token == '(':
                index += 1  # Skip '('
                node, index = parse_expression(index)
                index += 1  # Skip ')'
                return node, index
            else:
                node = parse_condition(" ".join(tokens[index:index+3]))  # 3 tokens per condition
                return node, index + 3

        root, _ = parse_expression(0)
        return root
    except Exception as e:
        raise Exception(f"Token Parsing Error: {e}")


# def create_rule(rule_string):
#     tokens = tokenize(rule_string)
#     ast = parse_tokens(tokens)
#     return ast

def create_rule(rule_string):
    try:
        tokens = tokenize(rule_string)
        ast = parse_tokens(tokens)
        return ast
    except ValueError as ve:
        raise ValueError(f"Rule Parsing Error: {ve}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while creating rule: {e}")



def combine_rules(rules, operator="AND"):
    """
    Combines multiple rules into a single AST using the specified logical operator.
    """
    if not rules:
        return None

    combined_ast = create_rule(rules[0])

    for rule in rules[1:]:
        rule_ast = create_rule(rule)
        combined_ast = Node('operator', left=combined_ast, right=rule_ast, value=operator)

    return combined_ast
