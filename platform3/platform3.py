#!/usr/bin/env python

import sys, threading

from services import main as services_main
from ui import main as ui_main

if __name__ == "__main__":

  try:
    print("Press CTRL-C to stop.")
    item = 0
    while True:
      t1 = threading.Thread(target=services_main, args=(), daemon=True)
      t1.start()

      t2 = threading.Thread(target=ui_main, args=(), daemon=True)
      t2.start()

      t1.join()
      t2.join()

  except KeyboardInterrupt:
    sys.exit(0)