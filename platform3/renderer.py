from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from typing import List

from models import Train

import constants

canvas = Image.new('RGB', (64, 32))

# Inflexible Constants
HEIGHT = 32
LINE_HEIGHT = 10
BULLET_WIDTH = LINE_HEIGHT
SPACING = 1
FONT = ImageFont.load_path("fonts/mta.pil")

# Flexible Constants
WIDTH = 64 # [Bullet][Flexible destination content][Countdown]
DESTINATION_REPEAT_GAP = 10 # Destination ticker loop gap between end of text and start of text
PAUSE_FRAMES = 50

def make_bullet(line_id: str) -> Image:
  line_id_to_bullet_map = {
    "1": constants.IRT_1_BULLET,
    "2": constants.IRT_2_BULLET,
    "3": constants.IRT_3_BULLET,
    "4": constants.IRT_4_BULLET,
    "5": constants.IRT_5_BULLET,
    "6": constants.IRT_6_BULLET,
    "7": constants.IRT_7_BULLET,
    "5X": constants.EXP_5_BULLET,
    "6X": constants.EXP_6_BULLET,
    "7X": constants.EXP_7_BULLET,
    "G": constants.G_BULLET,
    "J": constants.J_BULLET,
    "L": constants.L_BULLET,
  }
  return line_id_to_bullet_map.get(line_id, make_text(line_id, BULLET_WIDTH, draw_twice=False))

def make_row(bullet: Image, text: Image, countdown: Image) -> Image:
  row_canvas = Image.new('RGB', (WIDTH, LINE_HEIGHT))
  row_canvas.paste(bullet)
  row_canvas.paste(text, (BULLET_WIDTH + SPACING, 0))
  row_canvas.paste(countdown, (BULLET_WIDTH + text.width + SPACING * 2, 0))
  return row_canvas

# List must be <= 3 items
def make_final(rows: List[Image.Image]) -> Image:
  final = Image.new('RGB', (WIDTH, HEIGHT))
  for index in range(len(rows)):
    final.paste(rows[index], (0, (LINE_HEIGHT + SPACING) * index))
  return final

def make_text(text: str, destination_width: int, offset: int = 0, draw_twice = True) -> Image:
  text_canvas = Image.new('RGB', (destination_width, LINE_HEIGHT))

  draw = ImageDraw.Draw(text_canvas)
  draw.text((-offset, 0), text, font=FONT)
  if draw_twice:
    draw.text((text_width(text) + DESTINATION_REPEAT_GAP - offset, 0), text, font=FONT)
  return text_canvas

def make_countdown(text: str) -> Image:
  text_canvas = Image.new('RGB', (text_width(text), LINE_HEIGHT))

  draw = ImageDraw.Draw(text_canvas)
  draw.text((0, 0), text, font=FONT)
  return text_canvas

def text_width(text: str) -> int:
  width, _ = FONT.getsize(text)
  return width

@dataclass
class Countdown:
  bullet: Image
  destination: str
  arrivals: str

# countdowns must be <= 3 items
def make_animation(
  countdowns: List[Countdown],
  pause_frames: int
) -> List[Image.Image]:
  assert len(countdowns) <= 3, "Must have at most 3 items per animation"
  assert len(countdowns) >= 0, "Must have at least 1 item per animation"
  text_widths = list(map(lambda countdown: text_width(countdown.destination), countdowns))
  max_width = max(text_widths)
  images = []
  for index in range(max_width + DESTINATION_REPEAT_GAP + pause_frames):
    images.append(
      make_final(
        list(
          map(
            lambda countdown, width: make_frame_for_row(countdown, index, width),
            countdowns, text_widths
          )
        )
      )
    )
  return images

def make_frame_for_row(countdown: Countdown, index: int, text_width: int) -> Image:
  countdown_image = make_countdown(countdown.arrivals)
  destination_width = WIDTH - BULLET_WIDTH - countdown_image.width - SPACING * 2
  if text_width <= destination_width:
    return make_row(
      countdown.bullet,
      make_text(countdown.destination, destination_width, draw_twice=False),
      countdown_image
    )
  return make_row(
    countdown.bullet,
    make_text(countdown.destination, destination_width, 0 if index > text_width + DESTINATION_REPEAT_GAP else index),
    countdown_image
  )


def render(trains: List[List[Train]]) -> List[Image.Image]:
  first_trains: List[Train] = []
  for train_arrivals in trains:
    if train_arrivals:
      first_trains.append(train_arrivals[0])
  countdowns = list(
    map(
      lambda train: Countdown(
        make_bullet(train.line_id),
        train.terminus, str(train.eta)
      ),
      first_trains
    )
  )
  # partition countdowns so we show 3 at a time
  frames: List[Image.Image] = []
  partitioned_countdowns: List[List[Train]] = []
  for index in range(0, len(countdowns), 3):
    partitioned_countdowns.append(list(countdowns[index:index+3]))
  if partitioned_countdowns:
    for partitioned_countdown in partitioned_countdowns:
      frames += make_animation(
        partitioned_countdown,
        PAUSE_FRAMES
      )
    return frames
  else:
    return []