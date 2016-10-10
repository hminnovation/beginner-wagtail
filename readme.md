Beginner Wagtail
==================
A super straightforward implementation of Wagtail CMS.

# Installation
```
vagrant up
vagrant ssh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

# Apps included

- People
- Skills
- Location

# Purpose
This project is, loosely, based on a workshops @alexgleason and @heymonkeyriot gave in Philadelphia, March 2016. It's a consolidated basis for doing other workshops in a more logical way.
