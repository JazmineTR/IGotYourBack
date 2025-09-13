import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

DATA_FILE = "model/combined_dataset.xlsx"
LOG_REG_FILE = "log_reg_model.pkl"

def train_and_save():
    df = pd.read_excel(DATA_FILE)
    X = df[['lumbar_bipe', 'hip_bipe']]
    y = df['label']

    log_reg = LogisticRegression()

    log_reg.fit(X, y)

    joblib.dump(log_reg, LOG_REG_FILE)

    print("Models trained and saved.")

def predict_posture(lumbar_angle, hip_angle):
    model = joblib.load(LOG_REG_FILE)
    X_new = pd.DataFrame([[lumbar_angle, hip_angle]], columns=['lumbar_bipe', 'hip_bipe'])
    pred = model.predict(X_new)[0]
    prob = model.predict_proba(X_new)[0][1] 
    if pred == 1:
        return f"Dangerous ({prob*100:.1f}% confidence)"
    else:
        return f"Safe ({(1-prob)*100:.1f}% confidence)"

train_and_save()
print(predict_posture(35, 18))
print(predict_posture(28, 15))
print(predict_posture(19, 10))




