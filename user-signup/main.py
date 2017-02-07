#!/usr/bin/env python
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
    """
# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

username_signup = """
<form action="/" method="post" >
    <label>Username
    <input type="text" name="username" value="%(username)s" />
    <span class="error"> %(user_reprimand)s </span>
    </label>
<br>
    <label>Password
        <input type="password" name="password"  />
        <span class="error"> %(password_reprimand)s </span>
    </label>
<br>
    <label>Verify Password
        <input type="password" name="verify"  />
        <span class="error"> %(verify_reprimand)s </span>
    </label>
 <br>
    <label>Email (optional)
        <input type="text"  name="email" value="%(email)s" />
        <span class="error"> %(email_reprimand)s </span>
    </label>
<br>
    <input type="submit" value="signup"/>
</form>
"""

# welcome_page = """
# <!DOCTYPE html>
# <html>
# <head>
# <h2>Welcome</h2>
# </head>
# </html>
# """


def build_page(username="", user_reprimand="", password_reprimand="", verify_reprimand= "", email="",email_reprimand=""): #default empty argument
    initial_signup_page = page_header + username_signup + page_footer
    initial_signup_page = initial_signup_page % {"username":username,
                                                "user_reprimand":user_reprimand,
                                                "password_reprimand": password_reprimand,
                                                "verify_reprimand": verify_reprimand,
                                                "email":email,
                                                "email_reprimand":email_reprimand
                                                }

    return initial_signup_page

def welcome_page(username):
    header = "<h2>Welcome "
    if username:
        header = header + username
    header = header + "</h2>"
    return header

#ALIDATION FUNCTIONS SHOULD JUST RETURN TRUE OR FALSE
def valid_username(username):
    if (not username) or (username.strip() == "") : # spaces or nothing check
         return False
    return True

def valid_password(password):
    pattern = re.compile("^.{3,20}$")
    if pattern.match(password):
        return True
    return False

def valid_verify_password(password, verify_password):
    pattern = re.compile("^.{3,20}$")
    if (pattern.match(verify_password)) and (password == verify_password):
        return True
    return False

def valid_email(email):
    # look inside the request to figure out what the user typed
    if ("@" not in email and ".com" not in email and ".edu" not in email):
        return False
    return True #email



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(build_page())

    def post(self):

        uname = self.request.get("username")
        uname = cgi.escape(uname, quote=True)
        em = self.request.get("email")
        em = cgi.escape(em, quote=True)
        pw = self.request.get("password")
        vpw = self.request.get("verify")

        flag = False


        user_reprimand = ""
        if not valid_username(uname):
            user_reprimand = "Enter a valid username"
            user_reprimand = cgi.escape(user_reprimand, quote=True)
            flag = True

        password_reprimand = ""
        if not valid_password(pw):
            password_reprimand = "Need password!"
            password_reprimand = cgi.escape(password_reprimand, quote=True)
            flag = True

        verify_reprimand = ""
        if valid_password(pw):
            if not valid_verify_password(pw, vpw):
                verify_reprimand = "Passwords do not match!"
                verify_reprimand = cgi.escape(verify_reprimand, quote=True)
                flag = True

        email_reprimand = ""
        if em:
            if not valid_email(em):
                email_reprimand = "Invalid email"
                email_reprimand = cgi.escape(email_reprimand, quote=True)
                flag = True

        if flag == True:
            self.response.write(build_page(username=uname, user_reprimand=user_reprimand,
                                           password_reprimand=password_reprimand,
                                           verify_reprimand = verify_reprimand, email=em,
                                           email_reprimand=email_reprimand))

        else:
            self.redirect("/welcome?username=%s" % uname)  # redirect is ONLY GET requests



class Welcome(webapp2.RequestHandler):
    def get(self):
        u = self.request.get("username")
        self.response.write(welcome_page(u))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
