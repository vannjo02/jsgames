## The Rundown

This site uses SQLAlchemy to store user information and game scores. 
There are six tables in all, with a one to many relationship. 
We used the python module bcrypt to hash passwords, and it also is used to verify passwords, 
while protecting against time-attacks. 

There is a file called createdb.py which will create the sqlite database (or whatever the source is specified as)
file from scratch when it's run. 

There is some commented out code that was being used for protection against malicious redirects, 
at the suggestion of flask-login, but it wasn't working properly. 

WTForms is used to validate the forms for register, login, change password, and delete account. 

There is a small api system that can get accessed by calling one of:

/api/flappypong

/api/gravitygolf

/api/pacman

/api/fifteen

/api/lander


These will return all the scores for all users of one of the games.

I believe it is currently not set up with CORS. It's on the to-do list. 

## The Games

I took these games from open source sites like github, and the game 'Fifteen' was written by my roommate Ryne Hanson.
I edited the javascript games to make a couple of them harder, or easier, based entirely on my own opinions. In FlappyPong, I made 
the health decrease faster, in Lander I made it harder to crash the ship and also fixed the 'out of fuel' conditions. In Gravity Golf
I put a hole counter, and stroke counter at the top of the canvas, and reset the game after nine holes, before this it was just 
an infinitely looping game that increased the number of planets each round. I also drastically decreased the draw distance of the 
aiming line so that more skill was involved with guessing where it was going to land. Previously the line extended far enough out 
that the game was not challenging in the slightest because you could see exactly where it would land all the time.

Most of the games were easy enough to locate a score variable and send it to the server upon losing the game, or winning, but 
pacman was created in such a way that it was impossible for me to edit the javascript properly. So I used a mutation observer to 
check the CSS of the 'Game Over' text. That was the most interesting game to edit. 


## Issues

There was an issue with postgresql is causing problems with bcrypt on heroku. 
The issue has to do with the way psycopg2 stores text. To solve this, look at this stackoverflow answer:

http://stackoverflow.com/a/41441208/7055878

Use .decode('ascii') on the hashed password before storing into the database because of how psycopg2 stores
text. And then upon checking passwords, use password.encode('ascii'), to reverse the process. This works just fine with sqlite.

There's an issue with flask-login that causes really weird issues on heroku without adding this line in the procfile:

web: gunicorn app:app --preload

Source: http://stackoverflow.com/a/39768181/7055878

## Personal setup

If you'd like to use your personal heroku postgresql database, run this code in the command line while working with your project:

    heroku addons:create heroku-postgresql:hobby-dev

To get your database url:

    heroku config -s

To set up the relations in the database, copy that url, and paste it in the database.py file as the first argument in the 
'create_engine' line, (instead of 'local' or 'DATABASE_URI'). THEN run createdb.py and it will create the relations on that 
postgresql database. 

After that's done, uncomment this line:

    DATABASE_URI = os.environ['DATABASE_URL']

and replace the long url with 'DATABASE_URI'.
 

Joshua Vannatter,

Clinton Akomea-Agyin
