# score_manager.py
import json
import os

# Chemin vers le fichier JSON qui stockera les scores
SCORE_FILE_PATH = 'scores.json'

# Fonction pour ajouter un score
def add_score(player_name, score):
    scores = load_scores()
    scores.append({"name": player_name, "score": score})
    save_scores(scores)

# Fonction pour charger les scores depuis le fichier JSON
def load_scores():
    if os.path.exists(SCORE_FILE_PATH):
        with open(SCORE_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return []

# Fonction pour sauvegarder les scores dans le fichier JSON
def save_scores(scores):
    with open(SCORE_FILE_PATH, 'w') as file:
        json.dump(scores, file, indent=4)

# Fonction pour obtenir les scores triés
def get_top_scores(limit=10):
    scores = load_scores()
    top_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return top_scores[:limit]

# Fonction pour réinitialiser les scores
def reset_scores():
    save_scores([])
