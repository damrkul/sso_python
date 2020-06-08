# sso_python

## Overview
During an interview I was asked about how I would create a Single Sign On.   I thought it was an interesting topic, so I decided to give my self a quick excercise to see if I could do it.


I broke this application into 3 Parts.

- Authentication REST Service
- Website 1
- Website 2


I used Python for my Authentication Service  via Tornado module. 

I used PHP, with the Codeigniter framework (MVC) for my websites.  I could have used any other language, but I decided on this one because it is very quick to throw stuff together.


## Authentcation Server Database
There is no actual Database for this application.  I could easily add a MySQL or MongoDB but the point of this project wasn't really this, and wanted to focus on the actual SSO.    I am simply using a few python dictionary objects as my 'database' .



## How It works

So all in all the program works like this.

1) Website reaches out to the Authentication server, via POST,, and supplies a Username, Password, and a callback URL (this will be used to redirect the user back to the site.

2) Authentication recieves these, checks to see if username/password is found.   If found, it will redirect, user back to the site , supplying a Usertoken.

3) Website Recieves token.  Website creates a SESSION.    Token is added to Session.

4) Website will periodicatly check againstt he authentication server at  */check_login* endpoint each time goes to a new page to see if user is continued to be logged in 

5) If user decides to log out, he calls the /logout .  During this time, a POST call inside the website controller calls authentication */logout* which removes Cookie, and Token from the authentication database.   

6) Because The token has removed,  Any site that that goes to a new page, will force user to be logged out because */check_login* will return a token of *invalid*
 

### EndPoints 
The SSO RestAPI  has currently 7 endpoints.
```
        (r"/users", users),
        (r"/adduser", adduser),
        (r"/authenticate", authenticate),
        (r"/tokens", tokens),
        (r"/check_login", check_login),
        (r"/getuserinfo", getuserinfo),
        (r"/logout", logout),
```



## WebSites
I have 3 seperate webservers running with different domains.   The codebase are all identical.  The only thing I have had to change is the *application/config/config.php* and modify the *$config['base_url']*


*Current gits*:
https://github.com/damrkul/sso_python
https://github.com/damrkul/sso_website


Main Files to look at are here:

*Authentication Server:*
- https://github.com/damrkul/sso_python/blob/master/sso.py

*WebServer:*
- https://github.com/damrkul/sso_website/blob/master/application/controllers/App.php
- https://github.com/damrkul/sso_website/tree/master/application/views



###
