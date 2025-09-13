import pandas as pd

# Load your Excel file
df = pd.read_excel("model/S1Data.xlsx")   # replace with your actual file path

# Keep only the lumbar_bipe column
df_lumbar = df[["lumbar_bipe"]]

# Save to a new Excel file
df_lumbar.to_excel("lumbar_bipe_only.xlsx", index=False)

print("New file saved as lumbar_bipe_only.xlsx")