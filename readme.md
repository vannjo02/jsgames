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

There is an issue I'm running into with postgresql on heroku, such that the validate_password function in models.py 
is not running properly. The logs state that it's an error with bcrypt.
"TypeError: Unicode-objects must be encoded before hashing"
Which is strange because I AM encoding all the passwords before hashing. It works just fine with the sqlite database on heroku, 
but not postgresql. However, because of heroku's ephemeral system, the sqlite database gets erased whenever the server goes 
to sleep, which is why I attempted to transition to postgresql so that users and scores would remain. 

