def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    # If rules is a dict with a key "compliance_check", extract the list
    if isinstance(rules, dict) and "compliance_check" in rules:
        rules = rules["compliance_check"]

    # If report is string (PDF/TXT/DOCX)
    if isinstance(report, str):
        report_text = report.lower()
        for rule in rules:
            keyword = rule.get("keyword", "").lower()
            required = rule.get("must_exist", False)
            exists = keyword in report_text
            compliant = required == exists
            if compliant:
                passed += 1
            else:
                failed += 1
            results.append({
                "keyword": keyword,
                "must_exist": required,
                "exists": exists,
                "compliant": compliant,
                "description": rule.get("description", f"Check for keyword '{keyword}'"),
                "status": compliant
            })

    # If report is dict (JSON file)
    elif isinstance(report, dict):
        for rule in rules:
            field = rule.get("field") or rule.get("keyword", "")
            required = rule.get("must_exist", False)
            exists = field in report
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
                "description": rule.get("description", f"Check for field '{field}'"),
                "status": compliant
            })

    else:
        raise ValueError("Unsupported report format. Must be dict or string.")

    score = round((passed / (passed + failed)) * 100, 2) if (passed + failed) > 0 else 0
    return {
        "score": score,
        "passed": passed,
        "failed": failed,
        "rules": results
    }

def run_rule_engine(data, rules):
    return validate(data, rules)
