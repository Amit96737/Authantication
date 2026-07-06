from django.shortcuts import render
import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "models/model.pkl"), "rb"))
job_encoder = pickle.load(open(os.path.join(BASE_DIR, "models/job_encoder.pkl"), "rb"))
edu_encoder = pickle.load(open(os.path.join(BASE_DIR, "models/edu_encoder.pkl"), "rb"))

def ml_about_page(request):
    return render(request, "ml/ml_about_page.html", locals())

def salary_form(request):
    df = pd.read_csv(os.path.join(BASE_DIR, "Salary_data.csv"))

    jobs = df['Job Title'].dropna().unique()
    educations = df['Education Level'].dropna().unique()

    return render(request, "ml/form.html", {
        "jobs": jobs,
        "educations": educations
    })

def predict_salary(request):
    if request.method == "POST":

        age = int(request.POST['age'])
        job = request.POST['job']
        exp = float(request.POST['experience'])
        edu = request.POST['education']

        job_encoded = job_encoder.transform([job])[0]
        edu_encoded = edu_encoder.transform([edu])[0]

        result = model.predict([[age, job_encoded, exp, edu_encoded]])

        return render(request, "ml/result.html", {
            "salary": int(result[0])
        })

    return render(request, "ml/form.html")