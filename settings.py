WIDTH, HEIGHT = 900, 600
FPS = 60
TITLE = "Productivime"
BG_COLOR = (18, 18, 22)
FG_COLOR = (230, 230, 240)
ACCENT = (90, 130, 255)

HUD_HEIGHT = 60

# board
BOARD_MARGIN = 20
ZONE_BORDER = (70, 80, 110)
ZONE_FILL = (28, 30, 38)
ZONE_TITLE = (180, 190, 210)

# player
PLAYER_SIZE = (36, 36)
PLAYER_COLOR = (120, 200, 255)
PLAYER_SPEED = 260  # px/s

# Colors
ZONE_TODO_FILL = (255, 216, 168)   # #FFD8A8 — soft orange
ZONE_PROGRESS_FILL = (167, 197, 235)  # #A7C5EB — soft blue
ZONE_DONE_FILL = (183, 228, 199)   # #B7E4C7 — soft green

# Borders
ZONE_TODO_BORDER = (236, 190, 140)
ZONE_PROGRESS_BORDER = (146, 175, 214)
ZONE_DONE_BORDER = (160, 205, 180)

# Color titles
ZONE_TITLE = (40, 45, 55)



# Task card
TASK_SIZE = (120, 60)            # width x height of a task card
TASK_COLOR = (245, 245, 250)     # light card face
TASK_BORDER = (120, 125, 140)    # subtle border
TASK_TEXT = (40, 45, 55)         # text color on card

# Scoring
SCORE_TO_PROGRESS = 50
SCORE_TO_DONE = 100
PENALTY_SKIP_STAGE = 100


# Distractors
DISTRACTOR_WORDS = [
    "прокрастинация", "сорванный дедлайн", "забыл позвонить",
    "уведомления", "котики", "соцсети", "мессенджер", "зум-приглашение"
]
DISTRACTOR_COLOR = (230, 100, 140)  # readable on dark bg
DISTRACTOR_MIN_SPEED = 120
DISTRACTOR_MAX_SPEED = 220
DISTRACTOR_SPAWN_INTERVAL = 2.2    # seconds (starts)
DISTRACTOR_MIN_INTERVAL = 0.8      # cap difficulty
DISTRACTOR_DIFFICULTY_STEP = 0.15  # every X seconds reduce interval
DISTRACTOR_STEP_TIME = 25.0        # seconds between difficulty bumps

# Penalties and limits
PENALTY_HIT_DISTRACTOR = 50
MAX_ERRORS = 3

# Right-side spawn band (as fraction of width)
RIGHT_BAND_X_FRAC = 0.62  # spawn distractors to the right from this screen fraction