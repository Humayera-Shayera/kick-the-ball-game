"combo": 0,
"last_goal_time": 0,
now = time.time()
if now - game_state["last_goal_time"] < 10:  # within 10 sec
    game_state["combo"] += 1
else:
    game_state["combo"] = 1
game_state["last_goal_time"] = now
if game_state["combo"] > 1:
    draw_text(450, 750, f"Combo x{game_state['combo']}!", GLUT_BITMAP_HELVETICA_18)
