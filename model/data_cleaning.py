import pandas as pd

# Load both Excel files
df_lumbar = pd.read_excel("model/lumbar_bipe_only.xlsx")
df_hip = pd.read_excel("model/hip_bipe_only.xlsx")

# Combine side-by-side (assuming rows align)
df_combined = pd.concat([df_lumbar['lumbar_bipe'], df_hip['hip_bipe']], axis=1)

# New label: dangerous if either lumbar OR hip is dangerous
df_combined['label'] = ((df_lumbar['label'] == 1) | (df_hip['label'] == 1)).astype(int)

# Save new dataset
df_combined.to_excel("model/combined_dataset.xlsx", index=False)

print("Combined dataset saved as model/combined_dataset.xlsx")