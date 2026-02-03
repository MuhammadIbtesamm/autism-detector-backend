import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

df = pd.read_csv("train.csv")

features = df[['A1_Score','A2_Score','A3_Score','A4_Score','A5_Score',
               'A6_Score','A7_Score','A8_Score','A9_Score','A10_Score',
               'age']]

target = df['Class/ASD']

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)

scaler = StandardScaler()

X_train_age = scaler.fit_transform(X_train[['age']])
X_test_age = scaler.transform(X_test[['age']])

X_train = X_train.copy()
X_test = X_test.copy()

X_train['age'] = X_train_age
X_test['age'] = X_test_age

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n📊 Model Evaluation Results")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Model and scaler saved successfully!")
