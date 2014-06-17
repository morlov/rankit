import webapp2

import login 
import mainpage 
import newranking
import userpage
import sortranking

app = webapp2.WSGIApplication([
    ('/', mainpage.MainPage),
    ('/new', newranking.NewRanking),
    ('/sort/([0-9]+)', sortranking.SortRanking),
    ('/user/([a-zA-Z0-9_-]+)', userpage.UserPage),
    ('/signup', login.Signup),
    ('/signin', login.Signin),
    ('/signout', login.Signout)
    ], debug=True)
