# =========================
# IMPORTS
# =========================

import pygame
from sys import exit


# =========================
# GAME SETTINGS
# =========================

GAME_WIDTH = 512
GAME_HEIGHT = 512


# =========================
# PYGAME SETUP
# =========================

pygame.init()

Screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Quest for the Absolute")

clock = pygame.time.Clock()


# =========================
# LOAD IMAGES
# =========================

start_img = pygame.image.load(
    'Quest-for-the-Absolute/images/start.png'
).convert_alpha()

exit_img = pygame.image.load(
    'Quest-for-the-Absolute/images/exit.png'
).convert_alpha()


# =========================
# BUTTON CLASS
# =========================

class Button():

    def __init__(self, x, y, image, scale):

        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(
            image,
            (int(width * scale), int(height * scale))
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False


    def draw(self):

        action = False

        Screen.blit(
            self.image,
            (self.rect.x, self.rect.y)
        )

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1:

                if self.clicked == False:

                    self.clicked = True
                    action = True

        if pygame.mouse.get_pressed()[0] == 0:

            self.clicked = False

        return action


# =========================
# CREATE BUTTONS
# =========================

start_button = Button(
    50,
    200,
    start_img,
    0.8
)

exit_button = Button(
    350,
    200,
    exit_img,
    0.8
)


# =========================
# GAME VARIABLES
# =========================

game_started = False

inventory = []

current_town = "MossyBurrow"
current_area = "Home"
current_room = "Bedroom"

dialogue_active = False
dialogue_npc = None
dialogue_index = 0


# =========================
# WORLD
# =========================

world = {

    "MossyBurrow": {

        "Home": {

            "Bedroom": {

                "description":
                "You suddenly get shaken awake by your father.",

                "exits": {
                    "up": "Kitchen"
                },

                "npcs": []
            },

            "Kitchen": {

                "description":
                "Your father is standing in the kitchen.",

                "exits": {
                    "down": "Bedroom",
                    "right": "Living Room"
                },

                "npcs": ["father"]
            },

            "Living Room": {

                "description":
                "A small but comfortable living room.",

                "exits": {
                    "left": "Kitchen"
                },

                "npcs": []
            }
        }
    }
}


# =========================
# NPC DATA
# =========================

npcs = {

    "father": {

        "name": "Father",

        "dialogue": [

            {
                "text": "You finally woke up.",
                "next": 1
            },

            {
                "text": "We need to talk.",
                "next": 2
            },

            {
                "text": "What do you say?",

                "choices": [

                    {
                        "text": "What's happening?",
                        "next": 3
                    },

                    {
                        "text": "I'm listening.",
                        "next": 5
                    },

                    {
                        "text": "Let me sleep.",
                        "next": 7
                    }

                ]
            },

            {
                "text": "Something is wrong with the village.",
                "next": 4
            },

            {
                "text": "The village has been acting strange lately."
            },

            {
                "text": "Good. Then listen carefully.",
                "next": 6
            },

            {
                "text": "Something happened last night."
            },

            {
                "text": "There's no time for games.",
                "next": 8
            },

            {
                "text": "Fine, but you will regret this...."
            }

        ]
    }
}


# =========================
# MOVEMENT
# =========================

def move_player(direction):

    global current_room

    room = world[current_town][current_area][current_room]

    if direction in room["exits"]:

        current_room = room["exits"][direction]


# =========================
# GET CURRENT ROOM
# =========================

def get_current_room():

    return world[current_town][current_area][current_room]


# =========================
# FONT
# =========================

font = pygame.font.Font(None, 28)


# =========================
# DRAW BACKGROUND
# =========================

def draw():

    Screen.fill("dark green")


# =========================
# START DIALOGUE
# =========================

def start_dialogue(npc):

    global dialogue_npc
    global dialogue_index

    dialogue_npc = npc
    dialogue_index = 0


# =========================
# DRAW DIALOGUE
# =========================

def draw_dialogue():

    pygame.mouse.set_cursor(
        pygame.SYSTEM_CURSOR_ARROW
    )

    dialogue = npcs[dialogue_npc]["dialogue"][dialogue_index]

    line = dialogue["text"]

    name = font.render(
        npcs[dialogue_npc]["name"],
        True,
        "white"
    )

    Screen.blit(
        name,
        (40, 290)
    )

    text = font.render(
        line,
        True,
        "white"
    )

    Screen.blit(
        text,
        (40, 330)
    )

    if "choices" in dialogue:

        choices = dialogue["choices"]

        for i, choice in enumerate(choices):

            x = 40 + (i % 2) * 220
            y = 400 + (i // 2) * 55

            draw_choice(
                choice["text"],
                x,
                y
            )


# =========================
# DRAW CHOICE
# =========================

def draw_choice(text, x, y):

    rect = pygame.Rect(
        x,
        y,
        210,
        45
    )

    pygame.draw.rect(
        Screen,
        "dark gray",
        rect
    )

    choice_text = font.render(
        text,
        True,
        "white"
    )

    Screen.blit(
        choice_text,
        (x + 10, y + 10)
    )

    if rect.collidepoint(
        pygame.mouse.get_pos()
    ):

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND
        )


# =========================
# DRAW GAME
# =========================

def draw_game():

    Screen.fill("black")

    room = get_current_room()


# =========================
# MAIN GAME LOOP
# =========================

while True:

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        # =========================
        # CLOSE WINDOW
        # =========================

        if event.type == pygame.QUIT:

            pygame.quit()
            exit()


        # =========================
        # CHOICE CLICK
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_pos = pygame.mouse.get_pos()

                if dialogue_npc:

                    dialogue = npcs[dialogue_npc]["dialogue"][dialogue_index]

                    if "choices" in dialogue:

                        choices = dialogue["choices"]

                        for i, choice in enumerate(choices):

                            x = 40 + (i % 2) * 220
                            y = 400 + (i // 2) * 55

                            rect = pygame.Rect(
                                x,
                                y,
                                210,
                                45
                            )

                            if rect.collidepoint(
                                mouse_pos
                            ):

                                dialogue_index = choice["next"]


        # =========================
        # GAME EVENTS
        # =========================

        if game_started:

            if event.type == pygame.KEYDOWN:

              if event.key == pygame.K_SPACE:

                  dialogue = npcs[dialogue_npc]["dialogue"][dialogue_index]

                  if "next" in dialogue:

                     dialogue_index = dialogue["next"]


    # =========================
    # GAME STARTED
    # =========================

    if game_started:

        draw_game()

        if dialogue_npc:

            draw_dialogue()


    # =========================
    # MAIN MENU
    # =========================

    else:

        draw()

        # =========================
        # START BUTTON
        # =========================

        if start_button.draw():

            game_started = True

            start_dialogue("father")


        # =========================
        # EXIT BUTTON
        # =========================

        if exit_button.draw():

            pygame.quit()
            exit()


    # =========================
    # UPDATE SCREEN
    # =========================

    pygame.display.update()

    clock.tick(60)