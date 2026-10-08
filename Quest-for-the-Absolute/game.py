
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
    "Quest-for-the-Absolute/images/start.png"
).convert_alpha()

exit_img = pygame.image.load(
    "Quest-for-the-Absolute/images/exit.png"
).convert_alpha()


# =========================
# BUTTON CLASS
# =========================

class Button:

    def __init__(self, x, y, image, scale):

        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(
            image,
            (
                int(width * scale),
                int(height * scale)
            )
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self):

        action = False

        Screen.blit(
            self.image,
            self.rect
        )

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1:

                if not self.clicked:

                    self.clicked = True
                    action = True

        if pygame.mouse.get_pressed()[0] == 0:

            self.clicked = False

        return action


# =========================
# CREATE MENU BUTTONS
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

dialogue_npc = None
dialogue_index = "start"


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

        "dialogue": {

            "start": {

                "text": "You finally woke up.",

                "next": "talk"
            },

            "talk": {

                "text": "We need to talk.",

                "next": "question"
            },

            "question": {

                "text": "What do you say?",

                "choices": [

                    {
                        "text": "What's happening?",
                        "next": "whats_happening"
                    },

                    {
                        "text": "I'm listening.",
                        "next": "listening"
                    },

                    {
                        "text": "Let me sleep.",
                        "next": "sleep"
                    }
                ]
            },

            "whats_happening": {

                "text":
                "Something is wrong with the village.",

                "next": "village_strange"
            },

            "village_strange": {

                "text":
                "The village has been acting strange lately.",

                "next": "end"
            },

            "listening": {

                "text":
                "Good. Then listen carefully.",

                "next": "something_happened"
            },

            "something_happened": {

                "text":
                "Something happened last night.",

                "next": "end"
            },

            "sleep": {

                "text":
                "There's no time for games.",

                "next": "regret"
            },

            "regret": {

                "text":
                "Fine, but you will regret this..."
            },

            "end": {

                "text":
                "..."
            }
        }
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
# START DIALOGUE
# =========================

def start_dialogue(npc):

    global dialogue_npc
    global dialogue_index

    dialogue_npc = npc
    dialogue_index = "start"


# =========================
# FONT
# =========================

font = pygame.font.Font(None, 28)


# =========================
# DRAW MENU
# =========================

def draw():

    Screen.fill("dark green")


# =========================
# DRAW GAME
# =========================

def draw_game():

    Screen.fill("dark green")

    room = get_current_room()

    room_name = font.render(
        current_room,
        True,
        "white"
    )

    Screen.blit(
        room_name,
        (20, 20)
    )

    description = font.render(
        room["description"],
        True,
        "white"
    )

    Screen.blit(
        description,
        (20, 60)
    )


# =========================
# DRAW DIALOGUE
# =========================

def draw_dialogue():

    pygame.mouse.set_cursor(
        pygame.SYSTEM_CURSOR_ARROW
    )

    dialogue = npcs[dialogue_npc]["dialogue"][dialogue_index]

    dialogue_box = pygame.Rect(
        20,
        270,
        472,
        220
    )

    pygame.draw.rect(
        Screen,
        "black",
        dialogue_box
    )

    pygame.draw.rect(
        Screen,
        "white",
        dialogue_box,
        2
    )

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
        dialogue["text"],
        True,
        "white"
    )

    Screen.blit(
        text,
        (40, 330)
    )

    # =========================
    # DIALOGUE CHOICES
    # =========================

    if "choices" in dialogue:

        choices = dialogue["choices"]

        for i, choice in enumerate(choices):

            x = 40 + (i % 2) * 220
            y = 370 + (i // 2) * 55

            draw_choice(
                choice["text"],
                x,
                y
            )

    else:

        continue_text = font.render(
            "Click to continue",
            True,
            "gray"
        )

        Screen.blit(
            continue_text,
            (40, 400)
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

    if rect.collidepoint(
        pygame.mouse.get_pos()
    ):

        pygame.draw.rect(
            Screen,
            "gray",
            rect
        )

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND
        )

    else:

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


# =========================
# DRAW MOVEMENT BUTTONS
# =========================

def draw_movement_buttons():

    buttons = {}

    room = get_current_room()

    # UP
    if "up" in room["exits"]:

        buttons["up"] = pygame.Rect(
            221,
            360,
            70,
            45
        )

        pygame.draw.rect(
            Screen,
            "dark gray",
            buttons["up"]
        )

        text = font.render(
            "UP",
            True,
            "white"
        )

        Screen.blit(
            text,
            (238, 372)
        )

    # DOWN
    if "down" in room["exits"]:

        buttons["down"] = pygame.Rect(
            221,
            415,
            70,
            45
        )

        pygame.draw.rect(
            Screen,
            "dark gray",
            buttons["down"]
        )

        text = font.render(
            "DOWN",
            True,
            "white"
        )

        Screen.blit(
            text,
            (225, 427)
        )

    # LEFT
    if "left" in room["exits"]:

        buttons["left"] = pygame.Rect(
            130,
            415,
            70,
            45
        )

        pygame.draw.rect(
            Screen,
            "dark gray",
            buttons["left"]
        )

        text = font.render(
            "LEFT",
            True,
            "white"
        )

        Screen.blit(
            text,
            (138, 427)
        )

    # RIGHT
    if "right" in room["exits"]:

        buttons["right"] = pygame.Rect(
            312,
            415,
            70,
            45
        )

        pygame.draw.rect(
            Screen,
            "dark gray",
            buttons["right"]
        )

        text = font.render(
            "RIGHT",
            True,
            "white"
        )

        Screen.blit(
            text,
            (316, 427)
        )

    return buttons


# =========================
# MAIN GAME LOOP
# =========================

while True:

    for event in pygame.event.get():

        # =========================
        # CLOSE WINDOW
        # =========================

        if event.type == pygame.QUIT:

            pygame.quit()
            exit()

        # =========================
        # MAIN MENU
        # =========================

        if not game_started:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    # START GAME
                    if start_button.rect.collidepoint(mouse_pos):

                        game_started = True

                        # Father wakes you up immediately
                        start_dialogue("father")

                    # EXIT GAME
                    elif exit_button.rect.collidepoint(mouse_pos):

                        pygame.quit()
                        exit()

        # =========================
        # GAME
        # =========================

        else:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    # =========================
                    # DIALOGUE
                    # =========================

                    if dialogue_npc:

                        dialogue = npcs[dialogue_npc]["dialogue"][dialogue_index]

                        # -------------------------
                        # PLAYER HAS CHOICES
                        # -------------------------

                        if "choices" in dialogue:

                            for i, choice in enumerate(
                                dialogue["choices"]
                            ):

                                x = 40 + (i % 2) * 220
                                y = 370 + (i // 2) * 55

                                rect = pygame.Rect(
                                    x,
                                    y,
                                    210,
                                    45
                                )

                                if rect.collidepoint(mouse_pos):

                                    dialogue_index = choice["next"]

                        # -------------------------
                        # NORMAL DIALOGUE
                        # -------------------------

                        else:

                            if "next" in dialogue:

                                dialogue_index = dialogue["next"]

                            else:

                                # Dialogue is finished
                                dialogue_npc = None

                    # =========================
                    # MOVEMENT
                    # =========================

                    else:

                        movement_buttons = draw_movement_buttons()

                        for direction, rect in movement_buttons.items():

                            if rect.collidepoint(mouse_pos):

                                move_player(direction)

    # =========================
    # DRAW EVERYTHING
    # =========================

    if game_started:

        draw_game()

        if dialogue_npc:

            draw_dialogue()

        else:

            draw_movement_buttons()

    else:

        draw()

        start_button.draw()
        exit_button.draw()

    # =========================
    # UPDATE SCREEN
    # =========================

    pygame.display.update()

    clock.tick(60)
