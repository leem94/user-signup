#!/usr/bin/env python
import webapp2
import cgi

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

class MainHandler(webapp2.RequestHandler):
    def get(self):

        username_signup = """
        <form action="/add" method="post">
            <label>Username
            <input type="text" name="username" value="%(username)s" />
            </label>
        <br>


            <label>Password
            <input type="text" name="password" value="%(password)s" />
            </label>
            <br>


            <label>Verify Password
                <input type="password" name="verify" value="%(verifypassword)s" />
            </label>
            <br>


        <label>Email (optional)
        <input type="text"  name="email" value="%(email)s" />
        </label>
        <br>
        <input type="submit" value="signup" />
        </form>
        """

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        main_content = page_header + username_signup  + page_footer
        self.response.write(main_content)


class Validate(webapp2.RequestHandler):
    def valid_username(self):
        # look inside the request to figure out what the user typed
        user_name = self.request.get("username")

        if (not user_name) or (user_name.strip()== "") or (user_name.isspace()== True) : #spaces or nothing check
            error_message = "Enter a valid username" #create error message
            error_escaped = cgi.escape(error_message, quote=True)  #you need the quote #escape it
            self.redirect("/?error=" + error_escaped) #redirect it and add the escaped error message

    def valid_password(self):
        # look inside the request to figure out what the user typed
        pw = self.request.get("password")
        pw_verfy = self.request.get("verify")
        if (not pw == pw_verify):
            error_message = "Passwords do not match!"
            error_escaped = cgi.escape(error_message, quote=True)
            self.redirect("/?error=" + error_escaped)


    def valid_email(self):
        # look inside the request to figure out what the user typed
        email = self.request.get("email")
        if ("@" and ".com" not in email):    # .find????
            error_message = "Invalid email"
            error_escaped = cgi.escape(error_message, quote=True)
            self.redirect("/?error=" + error_escaped)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/', Validate)
], debug=True)
