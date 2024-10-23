from app.ast_logic import create_rule, combine_rules

def create_rule_manager(rule_string: str):
    return create_rule(rule_string)

def combine_rules_manager(rules: list[str], operator="AND"):
    return combine_rules(rules, operator)

def evaluate_rule_manager(rule_ast, data):
    return rule_ast.evaluate(data)
