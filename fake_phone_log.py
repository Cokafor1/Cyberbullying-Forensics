# make_fake_phone_log.py
import pandas as pd
import random
from datetime import datetime, timedelta
import sys

INPUT = "sample_bullying_data.csv"
OUTPUT = "fake_phone_log.csv"
BASE_LAT, BASE_LON = 40.7357, -74.1625  # adjust if you want different coords
RANDOM_SEED = 42
DAYS_SPAN = 20  # how many days to spread messages across

random.seed(RANDOM_SEED)

# Load input
try:
    df = pd.read_csv(INPUT)
except FileNotFoundError:
    print(f"ERROR: Could not find {INPUT} in the current folder.")
    sys.exit(1)

# Heuristically pick a text column (first object/string column)
text_cols = [c for c in df.columns if df[c].dtype == object]
if not text_cols:
    # fallback: use first column
    text_col = df.columns[0]
    print(f"No obvious text column found. Using first column: {text_col}")
else:
    # prefer common names
    preferred = [c for c in text_cols if c.lower() in ('tweet','text','message','tweet_text','content')]
    text_col = preferred[0] if preferred else text_cols[0]
    print(f"Using text column: {text_col}")

# Prepare rows
rows = []
start_time = datetime(2025, 10, 1, 8, 0, 0)

for i, (_, r) in enumerate(df.iterrows(), start=1):
    # random offset within DAYS_SPAN
    minutes_offset = random.randint(1, 60 * 24 * DAYS_SPAN)
    t = start_time + timedelta(minutes=minutes_offset)
    lat = BASE_LAT + random.uniform(-0.004, 0.004)
    lon = BASE_LON + random.uniform(-0.004, 0.004)
    message_text = str(r[text_col]).replace('\n', ' ').replace('\r', ' ').strip()

    # Randomly assign sender as Bully or Victim for variety (weight towards bully as sender)
    sender = random.choices(['Bully', 'Victim'], weights=[0.7, 0.3])[0]
    receiver = 'Victim' if sender == 'Bully' else 'Bully'

    rows.append({
        "message_id": i,
        "sender": sender,
        "receiver": receiver,
        "timestamp": t.strftime('%Y-%m-%d %H:%M:%S'),
        "message_text": message_text,
        "location_lat": round(lat, 6),
        "location_lon": round(lon, 6),
        "deleted_flag": int(random.random() < 0.2)  # ~20% messages marked deleted
    })

out = pd.DataFrame(rows)
# Sort by timestamp so timeline looks natural
out['timestamp_dt'] = pd.to_datetime(out['timestamp'])
out = out.sort_values('timestamp_dt').reset_index(drop=True)
out['message_id'] = out.index + 1
out = out.drop(columns=['timestamp_dt'])

out.to_csv(OUTPUT, index=False)
print(f"✅ Created {OUTPUT} with {len(out)} messages (saved in current folder).")
print("Open fake_phone_log.csv in DB Browser for SQLite or Excel to view the simulated phone log.")
