import webapp2

import scripts.login 
import scripts.mainpage 
import scripts.newranking
import scripts.userpage
import scripts.rankingpage

app = webapp2.WSGIApplication([
    ('/', scripts.mainpage.MainPage),
    ('/new', scripts.newranking.NewRanking),
    ('/ranking/([0-9]+)', scripts.rankingpage.RankingPage),
    ('/user/([a-zA-Z0-9_-]+)', scripts.userpage.UserPage),
    ('/signup', scripts.login.Signup),
    ('/signin', scripts.login.Signin),
    ('/signout', scripts.login.Signout)
    ], debug=True)
