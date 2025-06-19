import yaml
import json

def validate(report, rules):
    results = []
    passed = 0
    failed = 0

    is_structured = isinstance(report, dict) and "report_text" not in report

    for rule in rules:
        keyword = rule.get("keyword", "").lower()
        must_exist = rule.get("must_exist", False)
        description = rule.get("description", "")
        status = False

        if is_structured:
            status = any(keyword in str(value).lower() for value in report.values())
        else:
            # Here, handle text safely
            text = report["report_text"].lower() if isinstance(report, dict) else report.lower()
            status = keyword in text

        compliant = status == must_exist
        if compliant:
            passed += 1
        else:
            failed += 1

        results.append({
            "keyword": keyword,
            "must_exist": must_exist,
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

# 🔁 Called by Streamlit dashboard
def run_rule_engine(data, rules):
    return validate(data, rules)
