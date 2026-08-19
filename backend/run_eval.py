import json
import os
from .router import route
from .main import handle

def main():
    eval_path = os.path.join(os.path.dirname("backend/run_eval.py"), "eval_set.json")
    
    with open(eval_path, "r", encoding="utf-8") as f:
        eval_cases = json.load(f)
        
    passed = 0
    failed = 0
    
    for i, case in enumerate(eval_cases):
        question = case.get("question")
        repo_url = case.get("repo_url")
        expected_agent = case.get("expected_agent")
        expected_contains = case.get("expected_contains", "")
        
        # Check routing
        actual_agent = route(question)
        route_ok = actual_agent == expected_agent
        
        # Check handling/answer content
        answer = handle(repo_url, question)
        answer_lower = answer.lower() if isinstance(answer, str) else str(answer).lower()
        handle_ok = expected_contains.lower() in answer_lower
        case_passed = route_ok and handle_ok
        
        if case_passed:
            passed += 1
            print(f"[PASS] Case {i+1}: Route & Content matched.")
        else:
            failed += 1
            print(f"[FAIL] Case {i+1}: Route Match={route_ok}, Content Match={handle_ok}")
            print(f"       Expected Agent: {expected_agent}, Got: {actual_agent}")
            print(f"       Expected substring: '{expected_contains}'")

    print("\n=== EVALUATION SUMMARY ===")
    print(f"Total Passed: {passed}")
    print(f"Total Failed: {failed}")
    print(f"Total Cases : {passed + failed}")

if __name__ == "__main__":
    main()
