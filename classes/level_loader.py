import json

def load_level_data(difficulty):
    with open('levels.json', 'r') as file:
        levels = json.load(file)
    return levels.get(difficulty, levels["easy"])  # Default to "easy" if invalid input
