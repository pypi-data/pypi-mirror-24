# thelab-gauth

Note this is a public repo - do not commit private keys!

thelab-gauth is just a way to run Google Apps oauth with django-allauth.
It's public but is intended only as an example of how thelab does Google Auth

It includes a lovely django admin login override that shows a Sign in with google button!

## What it does

This package will link existing @thelabnyc.com google apps users to accounts. It will make a user when one does not already exist. If the user account with email already exists it the user will simply log in as this user (connecting the social auth to this django account).

It's also a place for instructions on adding auth for lab projects.

# Installation

1. pip install `thelab-gauth` and `django-allauth`
2. Add to INSTALLED_APPS 
```
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'labgauth'
```
3. Add to AUTHENTICATION_BACKENDS `allauth.account.auth_backends.AuthenticationBackend`
4. Add the following settings
```
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = 'labgauth.lab_adapter.SocialAccountAdapter'
```
5. In django admin go to `/admin/socialaccount/socialapp/` and create a new social application with your Google client ID and secret key.

# Development

Run `docker-compose up` for a sandbox environment