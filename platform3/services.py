from nyct_gtfs import NYCTFeed
import datetime, time
from typing import List

from config import key, stops
from constants import VALID_STOP_IDS
from models import Train
from memcache import set_arrivals

def main():
  # Validate config
  line_ids = set(map(lambda stop: stop.line_id, stops))
  assert line_ids.issubset(VALID_STOP_IDS), "Stop IDs is invalid"

  # Load the realtime feed from the MTA site
  line_id_to_feed_specifier = {
    "5X": "5",
    "6X": "6",
    "7X": "7",
    "FX": "F",
  }
  feeds = list(
    map(
      lambda stop: NYCTFeed(
        line_id_to_feed_specifier.get(stop.line_id, stop.line_id),
        api_key=key,
        fetch_immediately=False
      ),
      stops
    )
  )

  while True:
    arrivals: List[List[Train]] = []

    # Refresh live feeds
    for stop, feed in zip(stops, feeds):
      feed.refresh()
      trains = feed.filter_trips(line_id=stop.line_id)
      train_arrivals: List[Train] = []
      for train in trains:
        for update in train.stop_time_updates:
          if update.stop_id == stop.stop_id:
            # eta in floor minutes
            eta = int((update.arrival - datetime.datetime.now()).total_seconds() / 60)
            if eta > stop.min_walking_distance:
              train_arrivals.append(Train(stop.line_id, train.headsign_text, eta))
      arrivals.append(sorted(train_arrivals, key=lambda train: train.eta))

    set_arrivals(arrivals)

    # Wait 1 minute before polling again
    time.sleep(60)