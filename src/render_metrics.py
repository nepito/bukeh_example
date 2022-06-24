import pandas as pd
from jinja2 import Environment, FileSystemLoader
metrics = pd.read_csv("data/normalized_metrics.csv")

def get_str_metrics(index):
    mind_metrics = ["player_minutes", "goal_total", "goal_assists", "passes_key", "shots_on", "dribbles_success", "tackles_interceptions"]
    metrics_of_player_1 = list(metrics.loc[index][mind_metrics])
    str_player_1 = [str(metric) for metric in metrics_of_player_1]
    return str.join(', ', str_player_1)

fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

all_players = {f"player_{player+1}":get_str_metrics(player) for player in range(4)}
rendered = env.get_template("ejemplo_1.html").render(**all_players)
print(rendered)
