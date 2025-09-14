from posture_model import train_and_save, predict_posture, add_data_selftrain
import numpy as np
import pandas as pd
import joblib

train_and_save()

np.random.seed(42)  # reproducible
lumbar_vals = np.random.uniform(10, 50, 100)  # lumbar between 10–50
hip_vals = np.random.uniform(5, 25, 100)      # hip between 5–25
log_reg = joblib.load("log_reg_model.pkl")

df_synthetic = pd.DataFrame({
    "lumbar_bipe": lumbar_vals,
    "hip_bipe": hip_vals
})

# Save for later testing
'''
df_synthetic.to_excel("model/synthetic_test_points.xlsx", index=False)
print("Generated 100 synthetic test points.")

df = pd.read_excel("model/synthetic_test_points.xlsx")

for i, row in df.iterrows():
    result = predict_posture(row['lumbar_bipe'], row['hip_bipe'])
    add_data_selftrain(row['lumbar_bipe'], row['hip_bipe'])
    print(f"Point {i+1}: Lumbar={row['lumbar_bipe']:.1f}, Hip={row['hip_bipe']:.1f} → {result}")
'''

print(predict_posture(55, 10))