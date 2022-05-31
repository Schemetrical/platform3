import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from memcache import get_arrivals
from renderer import render

def main():
  # Configuration for the matrix
  options = RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 1
  options.parallel = 1
  # Should be set in DEFAULT_HARDWARE but just in case
  options.hardware_mapping = "adafruit-hat-pwm"

  matrix = RGBMatrix(options = options)
  time.sleep(2) # wait for first data pull

  images = []
  cached_arrivals = None
  while True:
    new_arrivals = get_arrivals()
    if cached_arrivals != new_arrivals:
      cached_arrivals = new_arrivals
      print(cached_arrivals)
      images = render(cached_arrivals)
    if images:
      print("displaying")
      for image in images:
        matrix.SetImage(image)
        time.sleep(1.0/30.0)
    else:
      print("polling")
      time.sleep(3) # poll until get image