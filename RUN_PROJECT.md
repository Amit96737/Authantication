PROJECT RUN STEPS

1. Clone the project in your PC
git clone <repo-link>
cd <project-folder>


2. Create virtual environment

For Windows:
python -m venv venv
.\venv\Scripts\activate

For Ubuntu:
sudo apt update
sudo apt install python3-venv -y
python3 -m venv env
source env/bin/activate


3. Install requirements
pip install -r requirements.txt


4. Setup database PostgreSQL
- Create database in PostgreSQL
- Add database credentials in .env file


5. Run migrations
python manage.py makemigrations
python manage.py migrate


6. Create superuser
python manage.py createsuperuser


7. Run project
python manage.py runserver


8. Run celery worker Ubuntu only
celery -A core worker -l info


Project will run on:
http://127.0.0.1:8000/