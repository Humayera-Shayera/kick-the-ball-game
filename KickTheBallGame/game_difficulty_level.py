game_difficulty = 'Medium'

difficulty_settings = {
    'Easy': {'opponent_speed': 0.2, 'super_duration': 10},
    'Medium': {'opponent_speed': 0.4, 'super_duration': 5},
    'Hard': {'opponent_speed': 0.6, 'super_duration': 3}
}

def set_difficulty(key):
    global game_difficulty
    if key == b'1':
        game_difficulty = 'Easy'
    elif key == b'2':
        game_difficulty = 'Medium'
    elif key == b'3':
        game_difficulty = 'Hard'

def get_opponent_speed():
    return difficulty_settings[game_difficulty]['opponent_speed']
