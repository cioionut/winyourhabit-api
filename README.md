# WinYourHabit API

### Setup
```bash
# clone repository
git clone git@github.com:cioionut/winyourhabit-api.git
cd winyourhabit-api

# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtualenv
pip install -r requirements.txt

# Install sqlite3, see django docs

# Create tables in database
python manage.py migrates

# Create superuser
python manage.py createsuperuser --email admin@example.com --username admin


```
### Run API
```bash
python manage.py runserver
```