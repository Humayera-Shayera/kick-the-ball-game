"stamina": 100.0,
"max_stamina": 100.0,


def update_stamina(is_moving):
    if is_moving:
        game_state["stamina"] = max(0, game_state["stamina"] - 0.5)
    else:
        game_state["stamina"] = min(game_state["max_stamina"], game_state["stamina"] + 0.3)
