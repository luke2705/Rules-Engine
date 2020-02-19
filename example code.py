# Example usage
import visio


Luke = visio.Person(850, 'Texas')
product = visio.Product('15 year')
rules = visio.load_rules()
engine = visio.RulesEngine(rules)

interest_rate = engine.run_rules(Luke,product)
if interest_rate is not None:
    print(f'Congrats, your approved interest rate is {interest_rate}!')
else:
    print(f"Unfortunately, we can't approve your request at this time.")