import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "Salary_data.csv")
df.dropna(inplace=True)

le_job = LabelEncoder()
le_edu = LabelEncoder()

df['Job Title'] = le_job.fit_transform(df['Job Title'])
df['Education Level'] = le_edu.fit_transform(df['Education Level'])

X = df[['Age', 'Job Title', 'Years of Experience', 'Education Level']]
y = df['Salary']

model = RandomForestRegressor()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(le_job, open("job_encoder.pkl", "wb"))
pickle.dump(le_edu, open("edu_encoder.pkl", "wb"))