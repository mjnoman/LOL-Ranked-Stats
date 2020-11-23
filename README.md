-This app is deployed via Heroku at https://lolrankedstats.herokuapp.com

-This App give some stats on ranked matches in League of Legends for specific players.

-This app requires the user to select the server they play on (NA for North America, EUW for Europe-West, KR for Korea, etc.) and the player's account name that they're looking up.

-This app will display their name, what ranked league they are in, what ranked division they are in, their current league points, their wins, their losses, and a list of their recently played champions, along with some number of recent matches and their stats.

-To run locally : Install Flask and create a Flask environment folder for this project and in main directory of project run the following shell commands:
...
source virtual/Scripts/activate
export FLASK_APP=app.py
flask run
...

You will also be required to run 'export api_key={your api key}'. This program needs a user's Riot api key if it's run locally.
