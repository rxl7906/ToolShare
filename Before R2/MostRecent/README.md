Tool Share
------------------------------------------------------------
Description:
Tool Share allows for neighbors in a community to share
tools among each other.
------------------------------------------------------------
B-Team: 
Erika Zuniga
John Rivera
Meghan OConner
Robin Li
------------------------------------------------------------
Required:
Django 1.6 +
Python 2.7 +
------------------------------------------------------------
Getting Started
To Run:
1. Open up the terminal, change to the toolshare directory
2. Start the dev server with 'python manage.py runserver' 
command.
------------------------------------------------------------
Minor Bugs/Defects:
1. For the signin and signup pages, more error messages are 
needed.

------------------------------------------------------------
Basic execution and usage instructions
To run the web application:
1. After downloading project materials, check root directory
of web application to see if a "db.sqlite3" file is there. 
If so, delete it before running application.
2. Open terminal and when you get into root directory, type in
"python manage.py syncdb" and a new database file should be 
created. Then fill in the requested info. 
3. Then type in "python manage.py runserver"
4. In the web browser, type in "localhost:8000" to see the 
index page. You can navigate to the sign in or the sign up page. 
5. For the sign up page, fill in the fields and a user object 
will be created. 
6. For the sign in page, sign in with the user object that 
was created previously. 
7. After signing in, you will be able to use the web app.
8. If you click on the toolshed, you will see what tools are 
in the database. There are tabs for adding a tool, borrowing a 
tool, and deleting a tool. The submission for adding a tool works 
however borrowing a tool and deleting a tool does not have working 
functionality. 
------------------------------------------------------------
