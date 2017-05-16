## The Rundown

This site uses SQLAlchemy to store use information and game scores. 
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

There is an issue I'm running into with postgresql on heroku, such that the transition from sqlite to postgresql is causing
problems with authentication, verifying passwords, etc. As per the advice of this stackoverflow answer:

http://stackoverflow.com/a/41441208/7055878

I decided to try to use .decode('ascii') on the hashed password before storing into the database because of how psycopg2 stores
text. And then upon checking passwords, I use password.encode('ascii'), to reverse the process. 

Things seem to be running ok, however there's still what appears to be a lot finnicky authentication with flask-login now. 
The system is retrieving data more slowly, or something, and flask-login sometimes returns that the user is anonymous,
and sometimes that they are logged in. This never happened with sqlite. 

I have also changed the password type from 'Text' to 'String'. This may be helping slightly, but the server is still seems 
to be unsure if someone is logged in at any given time, taking multiple refreshes to actually trigger the is_logged_in code. 

If one wanted to test this locally, just go to database.py and change 'DATABASE_URI' to the 'local' variable, 
and then comment out the DATABASE_URI line. 



In light of the problems above, I've just decided to have the heroku site running on sqlite so that it actually works properly,
even if users and scores get deleted all the time. 




Joshua Vannatter,

Clinton Akomea-Agyin
