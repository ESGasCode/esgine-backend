import yaml

def load_rule(regulator: str, base_path="parser/rules/unified_esg_rules.yaml"):
    """
    Load rule set by regulator prefix (e.g., FCA, SEC, SFDR, ISSB).
    """
    with open(base_path, "r") as file:
        all_rules = yaml.safe_load(file)

    regulator_rules = [
        rule for rule in all_rules
        if rule.get("regulation", "").lower().startswith(regulator.lower())
    ]

    return {
        "regulation": regulator.upper(),
        "compliance_check": regulator_rules
    }

