# Diabetes-Diagnostic-Assistant-Rule-based-Classification-Tool
🩺 Diabetes Classification System (Rule-Based)

A simple Python program that classifies a person's glucose regulation status based on ADA (American Diabetes Association) guidelines.

The system analyzes:

A1C %

Fasting Plasma Glucose (FPG)

2-hour OGTT value

Random Plasma Glucose (RPG) + symptoms

Pregnancy status

and returns one of the following:

✅ Normal
✅ Prediabetes
✅ Diabetes (probable)
✅ Gestational diabetes

📌 Features

✅ Rule-based medical classification
✅ Supports units: mg/dL and mmol/L
✅ Automatic unit conversion
✅ Handles missing values safely
✅ Input validation for numeric values
✅ Pregnancy detection and special output
✅ Loop for multiple patient analysis

🧠 How It Works

The program follows ADA diagnostic criteria:

Diabetes if ANY:

A1C ≥ 6.5%

FPG ≥ 126 mg/dL

OGTT ≥ 200 mg/dL

RPG ≥ 200 mg/dL with symptoms

Prediabetes if ANY:

A1C 5.7–6.4%

FPG 100–125 mg/dL

OGTT 140–199 mg/dL
