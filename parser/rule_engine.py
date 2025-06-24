import json

def get_nested_value(data, dotted_key):
    """Safely navigate nested dicts using dot notation like 'metrics.scope1'."""
    keys = dotted_key.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    for rule in rules.get("compliance_check", []):
        field = rule.get("keyword") or rule.get("field") or ""
        required = rule.get("must_exist", False)
        description = rule.get("description", f"Check for keyword '{field}'")

        if isinstance(report, dict):
            value = get_nested_value(report, field)
            exists = value is not None
        elif isinstance(report, str):
            exists = field.lower() in report.lower()
        else:
            exists = False

        compliant = required == exists

        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "field": field,
            "must_exist": required,
            "exists": exists,
            "compliant": compliant,
            "description": description,
            "status": compliant
        })

    score = round((passed / (passed + failed)) * 100, 2) if (passed + failed) > 0 else 0

    return {
        "score": score,
        "passed": passed,
        "failed": failed,
        "rules": results
    }

def run_rule_engine(data, rules):
    return validate(data, rules)
