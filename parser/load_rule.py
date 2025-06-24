import yaml

def load_rule(file_path, regulator=None):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    if regulator:
        # Filter rules for the selected regulator (FCA, SEC, SFDR, ISSB)
        filtered_rules = [
            rule for rule in data if rule.get("regulation", "").lower().startswith(regulator.lower())
        ]
        return {"compliance_check": filtered_rules}

    # Return all rules if no specific regulator is provided
    return {"compliance_check": data}
