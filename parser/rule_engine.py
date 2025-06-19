import yaml
import json

def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    # Handle both text and structured JSON reports
    text_data = ""
    if isinstance(report, dict) and "report_text" in report:
        text_data = report["report_text"].lower()
    elif isinstance(report, dict):
        text_data = json.dumps(report).lower()  # fallback for JSON
    elif isinstance(report, str):
        text_data = report.lower()  # plain string fallback

    for rule in rules:
        keyword = rule.get("keyword", "").lower()
        must_exist = rule.get("must_exist", False)
        description = rule.get("description", f"Check for keyword '{keyword}'")

        exists = keyword in text_data
        compliant = must_exist == exists

        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "keyword": keyword,
            "must_exist": must_exist,
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
