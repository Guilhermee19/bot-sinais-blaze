import json

def load_rules(file_path='assets/rules.json'):
    with open(file_path, 'r') as file:
        rules = json.load(file)
    return rules

def save_rules(rules, file_path='assets/rules.json'):
    with open(file_path, 'w') as file:
        json.dump(rules, file, indent=4)

def update_rule_points(rule_title, points):
    rules = load_rules()
    for rule in rules:
        if rule['title'] == rule_title:
            rule['points'] += points
            break
    save_rules(rules)

def predict_next_color(array):
    recent_colors = [obj['color'] for obj in array[-15:]]  # Considerando os últimos 15 registros
    rules = load_rules()
    
    for rule in rules:
        rule_pattern = rule['rule']
        if recent_colors[-len(rule_pattern):] == rule_pattern:
            return rule['next'].upper(), rule['title']

        return '-', None
   
