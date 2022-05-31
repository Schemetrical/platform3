from nyct_gtfs import NYCTFeed
import datetime, time
from typing import List

from config import key, stops
from models import Train
from memcache import set_arrivals

def main():
  # Load the realtime feed from the MTA site
  feeds = list(
    map(
      lambda stop: NYCTFeed(
        stop.line_id.value,
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
      trains = feed.filter_trips(line_id=stop.line_id.value)
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