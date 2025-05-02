def reset_ball_after_goal():
    x = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
    y = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
    game_state["ball_pos"] = [x, y, 0.0]
    game_state["ball_vel"] = [0.0, 0.0, 0.0]
