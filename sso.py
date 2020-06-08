import tornado.ioloop
import tornado.web
import json
import string
import random
from tornado import web, ioloop

users_list = {"jrankin": { "password": "jpass" , "firstname": "John" , "lastname": "Rankin", "location": "Eau Claire, WI" }}

tokenLength = 12
tokens_list = {}


class users(tornado.web.RequestHandler):

    def get(self):
        print self.request
        self.write(users_list)

class tokens(tornado.web.RequestHandler):

    def get(self):
        print self.request
        self.write(tokens_list)


class logout(tornado.web.RequestHandler):
    def get(self):
        username = ""
        #Clear Cookie
        token = self.get_cookie("token")
        self.clear_cookie("token")
        print "J:" + token 
        if token in tokens_list:
            username = tokens_list[token]

            users_list[username].pop("token")
            tokens_list.pop(token)
            print users_list[username]
            
        if 'Mozilla' in self.request.headers.get("User-Agent"):
            url = self.get_argument("url")
            self.redirect(url)
        else:
            self.write({ "reply": "You have been logged out."})
        



class adduser(tornado.web.RequestHandler):
    def post(self):
        print self.request
        username = self.get_argument("username")
        password = self.get_argument("password")
        firstname = self.get_argument("firstname")
        lastname = self.get_argument("lastname")
        location = self.get_argument("location")

        # Check for empty values
        if checkFields(username,password):
            return

        # Check if user already exists, will not add
        if checkIfUserExists(username):
            self.write({ "error": "username already exists"})
            return
        userinfo = { 
                "password": password,
                "firstname": firstname,
                "lastname": lastname,
                "location": location
        }

        users_list[username] = userinfo
        print users_list
        if 'Mozilla' in self.request.headers.get("User-Agent"):
            url = self.get_argument("url")
            self.redirect(url)
        else:
            self.write( username + ' has been added with password:'+ password )

class getuserinfo(tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        if token in tokens_list:
            username = tokens_list[token]
            self.write(users_list[username] )


class check_login(tornado.web.RequestHandler):
    def get(self):
        token = self.get_cookie("token")
        url = self.get_argument("url")
        if token is None:
            token = 'invalid'
        self.set_cookie("token", token)
        print "check_login:" +  str(token)
        self.redirect(url + '?token=' + token)

class authenticate(tornado.web.RequestHandler):
    def post(self):
        print self.request.headers
        token = ""
        username = self.get_argument("username")
        password = self.get_argument("password")
        if self.get_argument("username") in users_list:
            if users_list[username]['password'] == password:
                token = retrieveToken(username)
                
        if token is None:
            token = 'invalid'
            
        if 'Mozilla' in self.request.headers.get("User-Agent"):
            url = self.get_argument("url")

            #self.set_header("Set-Cookie: token=" + token , "")
            self.set_cookie("token", token)
            print "token:" + token 
            self.redirect(url + '?token=' + token)
        else: 
            self.write({ "username": username, "token" : token })

### Helpers
def retrieveToken(username):
    token = ""
    if username not in users_list:
        return

    if "token" in users_list[username]:
            token = users_list[username]['token']
    else:
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(tokenLength))

        tokens_list[token] = username

        users_list[username]['token'] = token
    return token


def checkIfUserExists(username):
    return  username in users_list

def checkFields(username,password):
    return   not username or not password


def make_app():
    return tornado.web.Application([
        (r"/users", users),
        (r"/adduser", adduser),
        (r"/authenticate", authenticate),
        (r"/tokens", tokens),
        (r"/check_login", check_login),
        (r"/getuserinfo", getuserinfo),
        (r"/logout", logout),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

