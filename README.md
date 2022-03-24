# Welcome to University of Exeter Hide and Seek!

NOTE: Do not refresh pages while running a lobby or game. The application does not currently support this and it could lead to unexpected errors.
NOTE: Because the site was designed for a mobile view, desktop browsers may be too wide, leading the map to cover the hider code. To fix this, resize the screen or zoom out.

### You can either install and run the app locally, or deploy it to your choice of server for production use. Follow the steps below to install and run:

# Local Deployment

## Install
1. Make a python virtual environment in this folder by running this in your console of choice:

        python -m venv env

2. Enter this by running an activate script:
    - env\Scripts\Activate.ps1 for Windows PowerShell
    - env\Scripts\activate.bat for Windows Command Prompt
    - env/bin/activate for Unix or MacOS

3. Move into .\campus_game_project\

4. Install dependencies by running the following:

        python -m pip install -r requirements.txt

5. Download and install Docker Desktop from the [Docker Website](https://www.docker.com/)

6. Run the following command to install and run a Redis image:

        docker run -p 6379:6379 -d redis:5

7. Finally, run the server with the following command:

        python manage.py runserver

## Usage
Go to http://127.0.0.1:8000/.

From here just create an account or sign in to an existing one, explore, and enjoy!

NOTE: To test joining with multiple players, use different browsers to ensure sessions do not overwrite each other.

# Production Deployment
NOTE: These instructions assume a use of the Google App Engine standard environment on Google Cloud Platform.

## Install
1. Download, install, and initialise the gcloud CLI using the [tutorial](https://cloud.google.com/sdk/docs/install).

2. Ensure instances of PostgreSQL and App Engine standard environment are set up correctly ([this tutorial is a good starting point](https://cloud.google.com/python/django/appengine)).

3. Move into .\campus_game_project\campus_game_project

4. Change the filename of the local settings.py to settings_local.py or remove the file for deployment.

5. Change the filename of settings_deploy.py to settings.py. (This ensures the settings are correct for deploying to the cloud.)

6. Move into .\campus_game_project\

7. Deploy the app with the following command:

        gcloud app deploy

## Usage
Go to https://hide-to-survive-app.nw.r.appspot.com/.

From here just create an account or sign in to an existing one, explore, and enjoy!

NOTE: To test joining with multiple players, use different browsers to ensure sessions do not overwrite each other.

# GameMaster Mode
To view the mode of GameMaster, a user with elevated rights who can manage all data, such as games, user accounts, and players, first create the GameMaster's credentials with the following command:

        python manage.py createsuperuser

Next, to log in, simply go to the app's URL followed by '/admin'. This will be either [local](http://127.0.0.1:8000/admin) or [deployed](https://hide-to-survive-app.nw.r.appspot.com/admin).