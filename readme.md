## Synopsis

This site uses SQLAlchemy to store use information and game scores. 
There are six tables in all, with a one to many relationship. 
We used the python module bcrypt to hash passwords, and we also used an equality algorithm 
that protects against time attacks, because flask-login suggested to do so. 

There is a file called createdb.py which will create the sqlite database file from scratch when it's run. 

There is some commented out code that was being used for protection against malicious redirects, 
at the suggestion of flask-login again, but it wasn't working properly. 

WTForms is used to validate the forms for register, login, change password, and delete account. 

There is a small api system that can get accessed by calling one of:
/api/flappypong
/api/gravitygolf
/api/pacman
/api/fifteen
/api/lander


These will return all the scores for all users of one of the games. 

There is an issue I'm running into with postgresql on heroku, such that the transition from sqlite to postgresql is causing
problems with authentication, verifying passwords, etc. As per the advice of this stackoverflow answer:

http://stackoverflow.com/a/41441208/7055878

I decided to try to use .decode('ascii') on the hashed password before storing into the database because of how psycopg2 stores
text. And then upon checking passwords, I use password.encode('ascii'), to reverse the process. 

Things seem to be running ok, however there's still what appears to be a lot finnicky authentication with flask-login now. 
The system is retrieving data more slowly, or something, and flask-login sometimes returns that the user is not anonymous,
and sometimes that they are logged in. This never happened with sqlite. 

If one wanted to test this locally, just go to database.py and change 'DATABASE_URI' to the 'local' variable, 
and then comment out the DATABASE_URI line. 
