import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
import os

DATA_FILE = "model/personalized_dataset.xlsx"
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
    
def add_data_selftrain(lumbar_angle, hip_angle, confidence_threshold=0.8):
    model = joblib.load(LOG_REG_FILE)
    X_new = pd.DataFrame([[lumbar_angle, hip_angle]], columns = ['lumbar_bipe', 'hip_bipe'])
    pred = model.predict(X_new)[0]
    prob = model.predict_proba(X_new)[0][1]
    confidence = prob if pred == 1 else 1 - prob
    
    if confidence >= confidence_threshold:
        df = pd.read_excel(DATA_FILE)
        new_point = {"lumbar_bipe": lumbar_angle, "hip_bipe": hip_angle, "label": pred}
        df = pd.concat([df, pd.DataFrame([new_point])], ignore_index= True)
        df.to_excel(DATA_FILE, index=False)
        train_and_save()

        print(f"Added new point (lumbar={lumbar_angle}, hip={hip_angle}) "
              f"as {'Dangerous' if pred==1 else 'Safe'} "
              f"({confidence*100:.1f}% confidence). Model retrained.")
    else:
        print(f"Skipped new point (lumbar={lumbar_angle}, hip={hip_angle}) "
              f"— confidence only {confidence*100:.1f}%.")

def reset_model():
    if os.path.exists("log_reg_model.pkl"):
        os.remove("log_reg_model.pkl")
    print("Model reset. Run train_and_save() to rebuild from dataset.")

