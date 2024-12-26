import json

def load_level_data(difficulty):
    with open('classes/levels.json', 'r') as file:
        levels = json.load(file)
    return levels.get(difficulty)
