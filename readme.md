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

# Troubleshooting
## Relationships
A person requires a relationship with a skill, employment status and location. It means that it's necessary to

 - Create a skills index page
 - Create a skills page (or several!)
 - Create a location index page
 - Create a location page (or several!)
 - Create an employment status (or several!)

Note: This will be fixed in the future with a fixtures file

## Existing homepage
Wagtail now comes with a homepage within the model. This unfortunately is not the same as the home app HomePage (`home.HomePage`) that the People, Skills and Location apps are expecting to be children of.

To get around this

 - Delete the homepage that arrives with Wagtail
 - Add the beginner wagtail homepage
 - Navigate to http://localhost:8000/admin/sites/ and add a new site
   - Title = localhost
   - Port = 80
   - Sitename = _Whatever you want_
   - Root Page = _Your new homepage_
   - Default = True

Note: This will be fixed in the future with a fixtures file