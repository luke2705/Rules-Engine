import json
from copy import copy


class Person:
    def __init__(self, credit_score, location, number_of_accounts=0):
        self.credit_score = credit_score
        self.location = location
        self.number_of_accounts = number_of_accounts
    
    def __repr__(self):
        return f'person with credit_score =  {self.credit_score}, location = {self.location}'


class Product:
    def __init__(self, name, interest_rate=5.0, disqualified=False):
        self.name = name
        self.interest_rate = interest_rate
        self.disqualified = disqualified

    def __repr__(self):
        return f'product with name = {self.name}, interest rate = {self.interest_rate}, disqualified = {self.disqualified}'


class RulesEngine:
    def __init__(self, rules):
        self.rules = rules

    def reload_rules(self, rules):
        self.rules = rules

    def run_rules(self, person, product):
        # In order to not impact the global interest rate/disqualification of a product, 
        # we create a copy to use with this person
        product = copy(product)
        for rule in self.rules:
            if eval(rule["condition"]):
                # Not all rules have parameters, but load them if they exist
                if rule.get("parameters") is not None:
                    # params gets used when dynamically executing actions
                    params = json.loads(rule["parameters"])

                exec(rule["action"])

        # This is outside the rule loop on the assumption that DQs are uncommon and running
        # through rules is quick. We could move it into the loop if it becomes worth it to
        # check for early breaking of the loop.
        if product.disqualified == True:
            # Depending on how this is consumed, we could alternatively have this return -1, 
            # but that seems confusing as it is a numeric value that could cause issues downstream
            return None
        else:
            # truncate python floats can sometimes return 5.000000000000005 instead of 5.00
            return "%0.2f" % product.interest_rate 


# this is a separate function instead of just being called directly in RulesEngine to allow rules 
# to be pulled from different sources or written in different ecosystems. The specific piece that 
# enables this is that the constructor for RulesEngine takes a rules parameter.
def load_rules():
    rules = [
        {  # Florida Disqualification
            'id': 1,
            'condition': '(person.location).lower()=="florida"',
            'action': 'product.disqualified=True'
        },
        {  # Good Credit Incentive
            'id': 2,
            'condition': 'person.credit_score >= 720',
            'action': 'product.interest_rate += params["interest_rate_delta"];',
            'parameters': '{"interest_rate_delta":-0.3}'
        },
        {  # Bad Credit Risk Compensation
            'id': 3,
            'condition': 'person.credit_score < 720',
            'action': 'product.interest_rate += params["interest_rate_delta"];',
            'parameters': '{"interest_rate_delta":0.5}'
        },
        {  # 7-1 ARM Adjustment
            'id': 4,
            'condition': '(product.name).lower() == "7-1 arm"',
            'action': 'product.interest_rate += params["interest_rate_delta"];',
            'parameters': '{"interest_rate_delta":0.5}'
        },
        {  # Returning Customer Discount
            'id': 5,
            'condition': 'person.number_of_accounts >= 1',
            'action': 'product.interest_rate += params["interest_rate_delta"];',
            'parameters': '{"interest_rate_delta":-0.1}'     
        }
    ]
    return rules
    