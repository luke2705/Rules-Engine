import visio
import pandas as pd


def run_tests(test_cases):
    passes = 0
    failures = 0
    for i, row in test_cases.iterrows():
        test_person = visio.Person(test_cases.credit_score[i], test_cases.location[i], test_cases.num_accounts[i])
        test_product = visio.Product(test_cases.product_name[i])
        # string casting here will allow us to catch 'None' as an expected result == to python's None
        result = str(engine.run_rules(test_person, test_product))
        if result != test_cases.expected_result[i]:
            failures += 1
            print(f'test {test_cases.test_name[i]} failed! Result = {result}, expected {test_cases.expected_result[i]}')
        else:
            passes += 1
    return passes, failures



# Unit Tests
test_cases = pd.read_csv('./Unit Tests.csv')
rules = visio.load_rules()
engine = visio.RulesEngine(rules)
total_passes = 0
total_failures = 0
for rule in rules:
    engine.reload_rules([rule])
    mask = test_cases['rule_id'] == rule["id"]
    passes, failures = run_tests(test_cases[mask])
    total_passes += passes
    total_failures += failures
print(f'Unit testing complete. {total_passes} passes, {total_failures} failures.')


# System Tests
test_cases = pd.read_csv('./System Tests.csv')
engine.reload_rules(rules)
passes, failures = run_tests(test_cases)
print(f'System testing complete. {passes} passes, {failures} failures.')

# Reverse the rules set to test whether order matters
rules = rules[::-1]
engine.reload_rules(rules)
passes, failures = run_tests(test_cases)
print(f'System testing with reversed rules set complete. {passes} passes, {failures} failures.')