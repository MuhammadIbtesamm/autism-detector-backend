import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("train.csv")

# Select features that match your app
features = df[['A1_Score','A2_Score','A3_Score','A4_Score','A5_Score',
               'A6_Score','A7_Score','A8_Score','A9_Score','A10_Score',
               'age']]

target = df['Class/ASD']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

# Scale age (important because age range is larger than 0/1 answers)
scaler = StandardScaler()
X_train.loc[:, 'age'] = scaler.fit_transform(X_train[['age']])
X_test.loc[:, 'age'] = scaler.transform(X_test[['age']])

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")


print("✅ Model and scaler saved successfully!")
