import yaml
import json

def validate(data, rules):
    results = []
    passed = 0
    failed = 0

    # If input is text (PDF/DOCX), wrap it in a dict with 'report_text' key
    if isinstance(data, str):
        data = {"report_text": data}

    for rule in rules:
        keyword = rule.get("keyword", "").lower()
        must_exist = rule.get("must_exist", False)
        description = rule.get("description", "No description provided")

        # Check if we're dealing with structured data (JSON) or raw text
        if "report_text" in data:
            report_text = data["report_text"].lower()
            exists = keyword in report_text
        else:
            exists = keyword in json.dumps(data).lower()

        compliant = must_exist == exists
        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "rule_id": rule.get("rule_id", "N/A"),
            "description": description,
            "must_exist": must_exist,
            "exists": exists,
            "compliant": compliant,
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

