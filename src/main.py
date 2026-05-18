import pandas as pd

input_file = "logs_KC Sandpit 2026_20260515-1122.csv"
output_file = "logs_KC Sandpit 2026_split_datetime.csv"

df = pd.read_csv(input_file)

# Split the first column into Date and Time
first_col = df.columns[0]
split_cols = df[first_col].astype(str).str.split(r'\s*,\s*', n=1, expand=True)

if split_cols.shape[1] != 2:
    raise ValueError("The first column did not split into exactly 2 parts.")

split_cols.columns = ["Date", "Time"]

# Keep remaining columns
df = pd.concat([split_cols, df.iloc[:, 1:].copy()], axis=1)

# Keep only rows where Component is exactly "Forum"
df = df[df["Component"].astype(str).str.strip() == "Forum"]

# Keep only specific Event name values
allowed_events = [
    "Discussion viewed",
    "Some content has been posted.",
    "Post created"
]

df = df[df["Event name"].astype(str).str.strip().isin(allowed_events)]

# Keep only rows where Event context contains "Forum: Collaborative Peer"
df = df[
    df["Event context"]
    .astype(str)
    .str.contains("Forum: Collaborative Peer", na=False)
]

# Save output
df.to_csv(output_file, index=False)

print(f"Done. Output saved to: {output_file}")