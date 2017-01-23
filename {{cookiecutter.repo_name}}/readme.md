{% raw %}
Beginner Wagtail
==================
A super straightforward implementation of Wagtail CMS.

# Installation locally
It should be sufficient to simply run `vagrant up` to load the project.
```
vagrant up
vagrant ssh
python manage.py runserver 0.0.0.0:8000
```

### Loading mock data
Given that it's a content management system it's quite useful to have some data :)

You can load it in by running
`python manage.py load_initial_data.py`

### Logging in
Once you've run `python manage.py load_initial_data.py` you'll be able to visit [http://localhost:8000/admin/](http://localhost:8000/admin/) and login using
Username: test
Password: password123

### Troubleshooting local installation problems
On the `vagrant up` command the vagrant/provision.sh file will run

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Occassionally (because the computer has gone to sleep etc) that process may not run smoothly. In that instance wait for `vagrant up` to complete, then `vagrant ssh` into the VM and run the above commands.

# Installation remotely
This project isn't designed to be deployed to a remote server, but rather for local playing and testing. An upcoming release will allow it to be deployed remotely.

# Apps included

- People
- Skills
- Location

# Purpose
This project is, loosely, based on a workshops @alexgleason and @heymonkeyriot gave in Philadelphia, March 2016. It's a consolidated basis for doing other workshops in a more logical way.

## Documentation
There is inline commenting through the project, but more details docs are planned for an upcoming release.
{% endraw %}
