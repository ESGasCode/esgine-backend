import yaml
import json

def run_rule_engine(data, rules):
    results = []
    passed = 0
    failed = 0

    is_text_based = isinstance(data, dict) and "report_text" in data
    report_text = data.get("report_text", "").lower() if is_text_based else ""

    for rule in rules:
        rule_id = rule.get("rule_id", "")
        description = rule.get("description", "")
        must_exist = rule.get("must_exist", True)
        keyword = rule.get("keyword", "").lower()
        field = rule.get("field", "")

        if is_text_based:
            exists = keyword in report_text if keyword else False
        else:
            value = data
            for key in field.split("."):
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    value = None
                    break
            exists = value is not None

        compliant = exists if must_exist else True

        results.append({
            "rule_id": rule_id,
            "description": description,
            "status": compliant
        })

        if compliant:
            passed += 1
        else:
            failed += 1

    score = (passed / len(rules)) * 100 if rules else 0
    return {
        "score": round(score, 2),
        "passed": passed,
        "failed": failed,
        "rules": results
    }
