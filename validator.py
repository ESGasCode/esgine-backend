import yaml
import json
from colorama import init, Fore, Style

init(autoreset=True)

def load_rules(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_disclosure(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_nested(data, field_path):
    keys = field_path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

def validate(disclosure, rules):
    results = []
    for rule in rules:
        field = rule["field"]
        must_exist = rule.get("must_exist", False)
        value = get_nested(disclosure, field)
        exists = value is not None
        compliant = exists if must_exist else True

        results.append({
            "rule_id": rule["rule_id"],
            "field": field,
            "compliant": compliant,
            "exists": exists,
            "value": value,
            "description": rule.get("description", "")
        })

    return results

def print_results(results, selected_regulator):
    print(f"\nValidation Results for: {selected_regulator.upper()}\n" + "-" * 50)

    for r in results:
        status = r["compliant"]
        symbol = f"{Fore.GREEN}✅ PASS" if status else f"{Fore.RED}❌ FAIL"
        print(f"{symbol}{Style.RESET_ALL} | {r['rule_id']}: {r['description']}")
        if not status:
            print(f"    ↳ Missing or invalid field: {r['field']}")

    total = len(results)
    passed = sum(r["compliant"] for r in results)
    print("\n" + "-" * 50)
    print(f"Summary: {Fore.CYAN}{passed}/{total} rules passed{Style.RESET_ALL}")

if __name__ == "__main__":
    print("Select a rule set to validate against:")
    print("Options: fca | sec | sfdr | issb")
    selected = input("Enter your choice: ").strip().lower()

    rule_paths = {
        "fca": ("rules/fca/fca-esg.yaml", "examples/sample_firmA.json"),
        "sec": ("rules/sec/sec-esg.yaml", "examples/sample_sec_firm.json"),
        "sfdr": ("rules/sfdr/sfdr-esg.yaml", "examples/sample_sfdr_firm.json"),
        "issb": ("rules/issb/issb-esg.yaml", "examples/sample_issb_firm.json")
    }

    if selected not in rule_paths:
        print(f"{Fore.RED}Invalid choice. Please enter one of: fca, sec, sfdr, issb{Style.RESET_ALL}")
        exit()

    rule_file, disclosure_file = rule_paths[selected]
    rules = load_rules(rule_file)
    disclosure = load_disclosure(disclosure_file)
    results = validate(disclosure, rules)
    print_results(results, selected)
