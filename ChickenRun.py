from asyncio import wait_for
import pgzrun
import random
from pgzero.keyboard import keyboard
from pgzhelper import *

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600

# Création du joueur et de la pièce avec une position aléatoire pour la pièce
player_character = Actor('p1_walk01.png', (260, 300))
coin = Actor('coingold.png', (random.randint(10, 790), 300))

# Création des tanks (ennemis) et mise à l'échelle
tanks = [
    {'actor': Actor('tank_dark.png', (100, 0)), 'speed': random.randint(4, 10)},
    {'actor': Actor('tank_red.png', (400, 0)), 'speed': random.randint(4, 10)},
    {'actor': Actor('tank_green.png', (700, 0)), 'speed': random.randint(4, 10)}
]
for tank in tanks:
    tank['actor'].scale = 4  # Mise à l'échelle des tanks

# Variables de jeu
life_points, score, game_over, speed_increased = 10, 0, False, False


# Fonction qui gère le déplacement du joueur
def move_player():
    if keyboard.left:
        player_character.x -= 5  # Déplacer le joueur à gauche
    if keyboard.right:
        player_character.x += 5  # Déplacer le joueur à droite

    # Gestion des limites de l'écran pour que le joueur réapparaisse de l'autre côté
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

        # Augmentation de la vitesse si le score est un multiple de 5 et que la vitesse n'a pas encore été augmentée
        if is_multiple_of_five(score) and not speed_increased:
            tank['speed'] += 1
            speed_increased = True  # Indique que la vitesse a été augmentée

        # Réinitialise l'augmentation de la vitesse quand le score n'est plus un multiple de 5
        if not is_multiple_of_five(score):
            speed_increased = False

        if not game_over:
            actor.y += speed  # Utilise la vitesse spécifique à chaque tank
            if actor.y > HEIGHT:
                actor.y = 0  # Réinitialise la position du tank s'il sort de l'écran

        # Si le joueur entre en collision avec un tank
        if player_character.colliderect(actor):
            life_points -= 1  # Perte de points de vie
            actor.y = 0  # Réinitialisation de la position du tank
            if life_points == 0:
                game_over = True  # Fin du jeu si les points de vie tombent à 0

        # Si le jeu est terminé, les tanks sont déplacés hors écran
        if game_over:
            actor.y = 1000


# Fonction qui gère la collision entre le joueur et la pièce
def update_coin():
    global score
    if coin.colliderect(player_character) and not game_over:
        score += 1  # Augmente le score lorsque le joueur récupère la pièce
        coin.x = random.randint(10, 790)  # Nouvelle position aléatoire pour la pièce


# Fonction principale de mise à jour du jeu (appelée à chaque frame)
def update():
    move_player()  # Mise à jour du déplacement du joueur
    move_tanks()  # Mise à jour du déplacement des tanks
    update_coin()  # Mise à jour de la position de la pièce et du score


# Fonction qui dessine les rectangles blancs sur l'écran
def draw_rects():
    for x in [250, 550]:  # Deux colonnes de rectangles
        for y in [0, 125, 295, 470]:  # Quatre rectangles verticaux par colonne
            screen.draw.filled_rect(Rect(x, y, 20, 75 if y == 0 else 120), (250, 250, 250))


# Fonction principale qui dessine l'état du jeu à l'écran
def draw():
    screen.fill((80, 80, 80))  # Fond gris
    if game_over:
        # Affichage du message de fin de jeu
        screen.draw.text(f'Game Over\nScore: {score}\nLifes: {life_points}', (360, 300), color=(255, 255, 255),
                         fontsize=60)
    else:
        draw_rects()  # Dessin des rectangles blancs
        # Affichage du score et des points de vie
        screen.draw.text(f'Score: {score}', (15, 10), color=(255, 255, 255), fontsize=30)
        screen.draw.text(f'Lifes: {life_points}', (100, 10), color=(255, 255, 255), fontsize=30)

        # Dessin des tanks, du joueur et de la pièce
        for tank in tanks:
            tank['actor'].draw()
        player_character.draw()
        coin.draw()


# Démarrage du jeu
pgzrun.go()