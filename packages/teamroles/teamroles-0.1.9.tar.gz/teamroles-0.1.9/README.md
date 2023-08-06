# Django Teams

django-teams simple implementation of user-role-team-permission network. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Require Django and Guardian

```
pip install django
pip install django-guardian
```

### Installing

After installing django and guardian,

add following line to INSTALLED_APPS in your ```settings.py``` file

```
'guardian'
```
and
```
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                                                  'guardian.backends.ObjectPermissionBackend')
```
This will allow to us to use guardian permission backend.
####Note: 
Above ```ModelBackend``` is not required but when you start project, django will
warn you to write this line in your settings.py.

Now we can install ```teamroles```

```
pip install teamroles
```
or specified version

```
pip install teamroles==0.1.x
```
You can see releases on github pages

After installation we should check something that is necessary
####First
Add  ```teamroles``` to INSTALLED_APPS in your settings.py file.
#####Second
Set ```AUTH_USER_MODEL = 'teamroles.User'``` if you want you packaged user model.

or you will get error. And you should choose one auth user model. django's initial for example
####The last thing we have to do to use mixins that come with package
Add following line to ```MIDDLEWARE``` in your settings.py file
```
    'teamroles.middleware.usermiddleware.CurrentUserMiddleware',
```

Now time to do migrate. When you perform migrate table automatically created in your db.

```Have fun```

## Built With

* [Django](https://docs.djangoproject.com/en/1.11/) - The web framework is used


## Versioning

For the versions available, see the [tags on this repository](https://github.com/mevlanaayas/django-teams/tags). 

## Authors

* **Mevlana** - *Initial work* - [mevlanaayas](https://github.com/mevlanaayas)

See also the list of [contributors](https://github.com/mevlanaayas/django-teams/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/mevlanaayas/django-teams/blob/master/LICENSE.txt) file for details

## Acknowledgements

* Hat tip to anyone who's code was used