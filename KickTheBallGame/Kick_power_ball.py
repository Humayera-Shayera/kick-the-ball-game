"kick_power": 0,
"charging_kick": False,


def handle_mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            game_state["charging_kick"] = True
        elif state == GLUT_UP:
            game_state["charging_kick"] = False
            perform_kick(game_state["kick_power"])
            game_state["kick_power"] = 0
            
if game_state["charging_kick"]:
    game_state["kick_power"] = min(100, game_state["kick_power"] + 1)
