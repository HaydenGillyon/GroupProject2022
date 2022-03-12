# Welcome to University of Exeter Hide and Seek!

NOTE: Do not refresh pages while running a lobby or game. The application does not currently support this and it could lead to unexpected errors.

### Follow the steps below to install and run:

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
From here just explore, using create to start a game and join to join one.

NOTE: To test joining with multiple players, use different browsers to ensure sessions do not overwrite each other.
