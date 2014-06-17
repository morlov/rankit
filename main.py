import webapp2

import scripts.login 
import scripts.mainpage 
import scripts.newranking
import scripts.userpage
import scripts.sortranking

app = webapp2.WSGIApplication([
    ('/', scripts.mainpage.MainPage),
    ('/new', scripts.newranking.NewRanking),
    ('/sort/([0-9]+)', scripts.sortranking.SortRanking),
    ('/user/([a-zA-Z0-9_-]+)', scripts.userpage.UserPage),
    ('/signup', scripts.login.Signup),
    ('/signin', scripts.login.Signin),
    ('/signout', scripts.login.Signout)
    ], debug=True)
