# Food Ordering Service API
This project is developed with django for educational purposes and should not
be used in production without checking for security issues and other important
stuff.

For running this on your computer first make sure you have `python3.6` or later
, then install `virtualenv` package.
```
pip install virtualenv
```

Create a virtual environment in main directory of the project (same folder as
 this file) preferably with a name like `venv`, `env`, `.venv` or `.env` so
`.gitignore` file can ignore it without any modification, I assumed you're
gonna use `.venv`.
```
virtualenv .venv
```

Activate your virtual environment:
```
source .venv/bin/activate
```

Or if you're still using windows:
```
.\venv\Scripts\activate
```

Then install all of the project's dependencies without affecting anything on your
computer.
```
pip install -r requirements.txt
```

Make migrations:
```
python manage.py makemigrations
```

Apply the created migrations:
```
python manage.py migrate
```

Create a super user, the terminal will ask for information itself.
```
python manage.py createsuperuser
```

Now you can run a Django development server, it will use port `8000` by
default:
```
python manage.py runserver
```

Login with your super user `username` and `password` at this url (I assumed
Django development server is running on the default port and you didn't
change it.):
```
http://127.0.0.1:8000/api/v1/api-auth/login/
```

Now, because you're a super user you can see all of the API documentations in
this url, if you visit this url while you are not a super user, you only see
APIs which you have access to.
```
http://127.0.0.1:8000/api/v1/documentation/
```
