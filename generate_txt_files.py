import pandas as pd
import os

# Input CSV
INPUT = "fake_phone_log.csv"
# Folder to save individual message files
OUTPUT_FOLDER = "messages_txt"

# Load the CSV
df = pd.read_csv(INPUT)

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Generate individual .txt files for each message
for idx, row in df.iterrows():
    filename = os.path.join(OUTPUT_FOLDER, f"msg_{row['message_id']}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Message ID: {row['message_id']}\n")
        f.write(f"Sender: {row['sender']}\n")
        f.write(f"Receiver: {row['receiver']}\n")
        f.write(f"Timestamp: {row['timestamp']}\n")
        f.write(f"Location: ({row['location_lat']}, {row['location_lon']})\n")
        f.write(f"Deleted Flag: {row['deleted_flag']}\n\n")
        f.write(f"Message Text:\n{row['message_text']}\n")

print(f"✅ Created {len(df)} txt files in '{OUTPUT_FOLDER}' folder.")
