import json
import random

def load_level_data(difficulty):
    with open('classes/game_metadata.json', 'r') as file:
        data = json.load(file)
    return data['levels'][difficulty]

def load_fruit_data():
    file = open("classes/game_metadata.json", 'r')
    data = json.load(file)
    return data["fruits"]
