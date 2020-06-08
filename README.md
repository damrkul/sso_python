# sso_python

This was a quick excercise where I was asked about Single Sign On (SSO).   I thought about it  for a bit and I thought it would be fun to see if I could get it done.


The way I've created this SSO was create a little service , via RestFul API.  I used Python Tornado as my webserver. 

So all in all the program works like this.

1) Website reaches out to the Authentication server, via POST,, and supplies a Username, Password, and a callback URL (this will be used to redirect the user back to the site.

2) Authentication recieves these, checks to see if username/password is found.   If found, it will redirect, user back to the site , supplying a Usertoken.

3) Website Recieves token.  Website creates a SESSION.    Token is added to Session.

4) Website will periodicatly check againstt he authentication server at  */check_login* endpoint each time goes to a new page to see if user is continued to be logged in 

5) If user decides to log out, he calls the /logout .  During this time, a POST call inside the website controller calls authentication */logout* which removes Cookie, and Token from the authentication database.   

6) Because The token has removed,  Any site that that goes to a new page, will force user to be logged out because */check_login* will return a token of *invalid*
 


The SSO RestAPI  has currently 7 endpoints.
````
        (r"/users", users),
        (r"/adduser", adduser),
        (r"/authenticate", authenticate),
        (r"/tokens", tokens),
        (r"/check_login", check_login),
        (r"/getuserinfo", getuserinfo),
        (r"/logout", logout),
```


Current gits:
https://github.com/damrkul/sso_python
https://github.com/damrkul/sso_website


## WebSites
Just to create a proof of concept,  I decided to use codeigniter which is a php Model-View-Controller framework.

I have 3 seperate webservers running with different domains.   The codebase are all identical.  The only thing I have had to change is the *application/config/config.php* and modify the *$config['base_url']*

Main Files to look at are here:
- https://github.com/damrkul/sso_website/blob/master/application/controllers/App.php
- https://github.com/damrkul/sso_website/tree/master/application/views



###
