import pandas as pd

# Load the dataset
df = pd.read_csv("cyberbullying_tweets.csv")

# Take a small random sample (e.g., 30 messages)
sample_df = df.sample(30, random_state=1)

# Save the smaller sample
sample_df.to_csv("sample_bullying_data.csv", index=False)

print(" Saved 30-sample dataset as sample_bullying_data.csv")
