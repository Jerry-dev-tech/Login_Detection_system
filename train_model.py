import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import matplotlib.pyplot as plt

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("Dataset/login_data.csv")

print("Dataset Loaded Successfully")
print(df.head())

# =====================================
# FEATURE ENGINEERING
# =====================================

# Extract Hour

df["Hour"] = (
    df["Login_Time"]
    .str.split(":")
    .str[0]
    .astype(int)
)

# Night Login

df["Night_Login"] = df["Hour"].apply(
    lambda x: 1 if x < 5 else 0
)

# Country Risk

country_risk = {

    "India": 0,
    "USA": 0,
    "UK": 0,

    "Russia": 1,
    "China": 1

}

df["Country_Risk"] = (
    df["Country"]
    .map(country_risk)
)

# Device Risk

device_risk = {

    "Laptop": 0,
    "Desktop": 0,
    "Mobile": 0,

    "Unknown": 1
}

df["Device_Risk"] = (
    df["Device"]
    .map(device_risk)
)

# =====================================
# FEATURES
# =====================================

X = df[

    [

        "Hour",

        "Night_Login",

        "Login_Success",

        "Failed_Attempts",

        "Country_Risk",

        "Device_Risk"

    ]

]

y = df["Suspicious"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# =====================================
# RANDOM FOREST
# =====================================

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

print("\nRandom Forest Training Completed")

# =====================================
# PREDICTION
# =====================================

# =====================================
# PREDICTION & EVALUATION
# =====================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print("\n========== MODEL PERFORMANCE ==========")
print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1-Score :", round(f1 * 100, 2), "%")

print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(y_test, predictions))

print("\n========== CONFUSION MATRIX ==========")
print(confusion_matrix(y_test, predictions))

# =====================================
# SAVE MODEL
# =====================================

os.makedirs(

    "models",

    exist_ok=True

)

joblib.dump(

    model,

    "models/model.pkl"

)

# =====================================
# SAVE ACCURACY
# =====================================

with open("models/performance.txt", "w") as f:
    f.write(f"Accuracy : {round(accuracy*100,2)}%\n")
    f.write(f"Precision: {round(precision*100,2)}%\n")
    f.write(f"Recall   : {round(recall*100,2)}%\n")
    f.write(f"F1-Score : {round(f1*100,2)}%\n")

print("\nModel Saved Successfully")

# =====================================
# FEATURE IMPORTANCE
# =====================================

features = X.columns

importance = model.feature_importances_

plt.figure(figsize=(8,5))

plt.bar(

    features,

    importance

)

plt.title(

    "Random Forest Feature Importance"

)

plt.xlabel(

    "Features"

)

plt.ylabel(

    "Importance"

)

plt.tight_layout()

os.makedirs(

    "static",

    exist_ok=True

)

plt.savefig(

    "static/feature_importance.png"

)

print(

    "\nFeature Importance Chart Saved"

)

# =====================================
# SAMPLE TEST
# =====================================

sample_login = [[

    2,  # Hour

    1,  # Night Login

    1,  # Login Success

    5,  # Failed Attempts

    1,  # Country Risk

    1   # Device Risk

]]

result = model.predict(

    sample_login

)

if result[0] == 1:

    print("\n⚠ Suspicious Login")

else:

    print("\n✅ Normal Login")