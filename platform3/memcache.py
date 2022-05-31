import threading

from typing import List
from models import Train

lock = threading.Lock()
arrivals: List[List[Train]] = []

def set_arrivals(new_arrivals: List[List[Train]]):
  global arrivals
  lock.acquire()
  arrivals = new_arrivals
  lock.release()

def get_arrivals() -> List[List[Train]]:
  global arrivals
  lock.acquire()
  ret_val = arrivals
  lock.release()
  return ret_val
