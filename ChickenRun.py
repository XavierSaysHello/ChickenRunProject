from asyncio import wait_for
import pgzrun
import random
from pgzero.keyboard import keyboard
from pgzhelper import *
import ChickenRunScore  # Importation du système de gestion de scores

# Demande le nom du joueur avant de démarrer le jeu
username = input("Please enter your name: ")

# Taille de la fenêtre
WIDTH, HEIGHT = 1000, 700

# Création du joueur et de la pièce avec une position au centre de l'écran
player_character = Actor('p1_walk01.png', (WIDTH // 2, HEIGHT // 2))
coin = Actor('coingold.png', (WIDTH // 2, HEIGHT // 2))

# Création des tanks (ennemis) et mise à l'échelle
tanks = [
    {'actor': Actor('tank_dark.png', (100, 0)), 'speed': random.randint(4, 10)},
    {'actor': Actor('tank_red.png', (500, 0)), 'speed': random.randint(4, 10)},
    {'actor': Actor('tank_green.png', (900, 0)), 'speed': random.randint(4, 10)}
]
for tank in tanks:
    tank['actor'].scale = 4  # Mise à l'échelle des tanks

# Variables de jeu
life_points, score, game_over, speed_increased = 20, 0, False, False
show_score_page = False  # Pour contrôler l'affichage de la page des scores

# Fonction pour redémarrer le jeu
def restart_game():
    global life_points, score, game_over, speed_increased, tanks, show_score_page
    life_points, score, game_over, speed_increased = 20, 0, False, False
    show_score_page = False  # Réinitialiser la page des scores
    for tank in tanks:
        tank['actor'].y = 0
        tank['speed'] = random.randint(1, 6)

# Fonction qui gère le déplacement du joueur
def move_player():
    if keyboard.left:
        player_character.x -= 5
    if keyboard.right:
        player_character.x += 5

    if player_character.x > WIDTH:
        player_character.x = 0
    if player_character.x < 0:
        player_character.x = WIDTH

# Fonction pour vérifier si le score est un multiple de 5
def is_multiple_of_five(value):
    return value > 0 and value % 5 == 0

# Fonction qui gère le déplacement des tanks et les collisions avec le joueur
def move_tanks():
    global life_points, game_over, speed_increased
    for tank in tanks:
        actor, speed = tank['actor'], tank['speed']

        if is_multiple_of_five(score) and not speed_increased:
            tank['speed'] += 1
            speed_increased = True

        if not is_multiple_of_five(score):
            speed_increased = False

        if not game_over:
            actor.y += speed
            if actor.y > HEIGHT:
                actor.y = 0

        if player_character.colliderect(actor):
            life_points -= 1
            actor.y = 0
            if life_points == 0:
                game_over = True
                # Enregistre le score du joueur avec le nom
                ChickenRunScore.add_score(username, score)

        if game_over:
            actor.y = 1000

# Fonction qui gère la collision entre le joueur et la pièce
def update_coin():
    global score
    if coin.colliderect(player_character) and not game_over:
        score += 1
        coin.x = random.randint(10, WIDTH - 10)

# Fonction principale de mise à jour du jeu
def update():
    if not game_over:
        move_player()
        move_tanks()
        update_coin()
    else:
        if keyboard.r:  # Relance le jeu si la touche "R" est appuyée
            restart_game()
        if keyboard.s:  # Accède à la page des scores si "S" est appuyée
            global show_score_page
            show_score_page = True

# Fonction qui dessine les rectangles blancs sur l'écran
def draw_rects():
    for x in [300, 700]:  # Positions X mises à jour
        for y in [0, 125, 295, 470]:
            screen.draw.filled_rect(Rect(x, y, 20, 75 if y == 0 else 120), (250, 250, 250))

# Fonction principale qui dessine l'état du jeu
def draw():
    screen.fill((80, 80, 80))
    if game_over and not show_score_page:
        screen.draw.text(f'Game Over\nScore: {score}', (400, 200), color=(255, 255, 255), fontsize=60)
        screen.draw.text("Press 'R' to Restart", (400, 500), color=(255, 255, 255), fontsize=30)
        screen.draw.text("Press 'S' for Scores", (400, 550), color=(255, 255, 255), fontsize=30)
    elif show_score_page:
        # Affiche les meilleurs scores
        screen.draw.text("Top 10 Scores", (400, 50), color=(255, 255, 255), fontsize=60)
        top_scores = ChickenRunScore.get_top_scores()
        for i, score_data in enumerate(top_scores):
            screen.draw.text(f"{score_data['name']}: {score_data['score']}", (400, 150 + i * 30),
                             color=(255, 255, 255), fontsize=30)
        screen.draw.text("Press 'R' to Go Back", (400, 600), color=(255, 255, 255), fontsize=30)
    else:
        draw_rects()
        screen.draw.text(f'Score: {score}', (15, 10), color=(255, 255, 255), fontsize=30)
        screen.draw.text(f'Lifes: {life_points}', (100, 10), color=(255, 255, 255), fontsize=30)
        for tank in tanks:
            tank['actor'].draw()
        player_character.draw()
        coin.draw()

# Démarrage du jeu
pgzrun.go()
