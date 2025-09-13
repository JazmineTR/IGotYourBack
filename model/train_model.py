import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score


df_lumbar = pd.read_excel("model/lumbar_bipe_only.xlsx")
df_hip = pd.read_excel("model/hip_bipe_only.xlsx")
df = pd.concat([df_lumbar['lumbar_bipe'], df_hip['hip_bipe']], axis = 1)
df['label'] = ((df_lumbar['label'] == 1) | (df_hip['label'] == 1)).astype(int)
X = df[['lumbar_bipe', 'hip_bipe']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

coef_lumbar = log_reg.coef_[0][0]
coef_hip = log_reg.coef_[0][1]
intercept = log_reg.intercept_[0]
lumbar_test = 33
hip_cutoff = -(coef_lumbar * lumbar_test + intercept) / coef_hip
print(f"At lumbar {lumbar_test}°, hip cutoff ≈ {hip_cutoff:.2f}°")

print(f"Logistic Regression coefficients → lumbar: {coef_lumbar:.2f}, hip: {coef_hip:.2f}")
print(f"Intercept = {intercept:.2f}")

scores = cross_val_score(log_reg, X, y, cv=5)
print("Logistic CV scores:", scores, "Mean:", scores.mean())

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n=== Random Forest Report ===")
print(classification_report(y_test, y_pred_rf))

hip_thresholds = []
for tree in rf.estimators_:
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold
    # Find splits on hip_bipe (feature index 1)
    hip_thresholds.extend(threshold[feature == 1])

hip_thresholds = [t for t in hip_thresholds if t != -2]  # remove unused
print("Random Forest hip_bipe cutoffs:", np.unique(np.round(hip_thresholds, 2)))

first_tree = rf.estimators_[0].tree_
threshold_rf = first_tree.threshold[0]
feature_rf = first_tree.feature[0]
print(f"First split: feature = {feature_rf}, threshold = {threshold_rf:.2f}")


scores = cross_val_score(log_reg, X, y, cv=5)
print("Random Forest CV scores:", scores, "Mean:", scores.mean())

# --- Logistic Regression Hip Cutoff Table ---
print("\nHip cutoff table (from Logistic Regression)")
print("Lumbar° | Hip cutoff°")
print("----------------------")

for lumbar_val in [30, 32, 34, 36, 38, 40]:
    hip_cutoff = -(coef_lumbar * lumbar_val + intercept) / coef_hip
    print(f"{lumbar_val:7.0f} | {hip_cutoff:10.2f}")