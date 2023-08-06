=====
django-esay-account
=====

django-esay-account is a simple Django app for accounts handle login & SingUp & logout and User Profil tow



Quick start
-----------

1. Add "django-esay-account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
    'crispy_forms',
    'account',
    ]
  add this line for the crispy_froms

	CRISPY_TEMPLATE_PACK = 'bootstrap3'

2. Include the account URLconf in your project urls.py like this::

    url(r'^', include('account.urls')),
    

3. add this 6 lines at the bottom in the settings files to handel the password reset.

	EMAIL_BACKEND ='django.core.mail.backends.console.EmailBackend' 
	DEFAULT_FROM_EMAIL = 'example@example.com'
	EMAIL_HOST_USER = ''
	EMAIL_HOST_PASSWORD = ''
	EMAIL_USE_TLS = False 
	EMAIL_PORT = 1025
   
   and 
   
  MEDIA_URL = '/media/'

4. Run `python manage.py migrate` to create the django-esay-account models.


5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a django-esay-account (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/login/ to test the  django-esay-account.