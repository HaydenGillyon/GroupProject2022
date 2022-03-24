# !-- Not using gunicorn or WSGI FOR DEPLOYMENT --!
# from campus_game_project.wsgi import application

# app = application
# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This file imports the WSGI-compatible object of your Django app,
# application from mysite/wsgi.py and renames it app so it is discoverable by
# App Engine without additional configuration.
# Alternatively, you can add a custom entrypoint field in your app.yaml:
# entrypoint: gunicorn -b :$PORT mysite.wsgi
#
# !-- Using Daphne and ASGI FOR DEPLOYMENT --!
# The following documents help describe the method behind using ASGI in Django.
# https://channels.readthedocs.io/en/latest/asgi.html
# https://channels.readthedocs.io/en/latest/deploying.html
