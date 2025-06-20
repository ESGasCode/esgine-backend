import re

def validate(data, rules):
    results = []
    passed = 0
    failed = 0

    # Determine if data is dict (JSON) or str (text from PDF/DOCX)
    if isinstance(data, dict):
        is_json = True
    elif isinstance(data, str):
        is_json = False
    elif isinstance(data, dict) and "report_text" in data:
        is_json = False
        data = data.get("report_text", "")
    else:
        raise ValueError("Unsupported data type for validation")

    for rule in rules:
        keyword = rule.get("keyword", "").lower()
        required = rule.get("must_exist", False)
        description = rule.get("description", "No description provided.")
        rule_id = rule.get("rule_id", "unknown")

        if is_json:
            # For structured data (JSON)
            exists = any(keyword in str(value).lower() for value in data.values())
        else:
            # For unstructured text
            exists = keyword in data.lower()

        compliant = required == exists
        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "rule_id": rule_id,
            "keyword": keyword,
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
