import yaml
import json

def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    for rule in rules.get("compliance_check", []):
        # Support both 'field' and 'keyword' for compatibility
        field = rule.get("keyword") or rule.get("field") or ""
        required = rule.get("must_exist", False)
        description = rule.get("description", f"Check for keyword '{field}'")

        # Handle JSON (dict) input
        if isinstance(report, dict):
            # Case-insensitive key check
            exists = any(field.lower() == key.lower() for key in report.keys())

        # Handle extracted text (str) input
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
