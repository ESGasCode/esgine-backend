import yaml
import json

def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    # Determine if input is structured JSON (dict) or text (str)
    is_structured = isinstance(report, dict) and "report_text" not in report

    for rule in rules:
        keyword = rule.get("keyword", "").lower()
        must_exist = rule.get("must_exist", False)
        description = rule.get("description", "")
        rule_id = rule.get("rule_id", "unknown")

        if is_structured:
            # JSON: check if the key exists in the report
            exists = keyword in report
        else:
            # Text: check if keyword exists in the uploaded text
            text = report.get("report_text", "").lower()
            exists = keyword in text

        compliant = (exists == must_exist)

        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "rule_id": rule_id,
            "description": description,
            "status": compliant,
            "must_exist": must_exist,
            "found": exists
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
