import handler
import database
import json
import time

class NewRanking(handler.Handler):

    def get(self):
        user_name = self.get_current_user()
        if user_name:
            self.render("new.html", user_name=user_name)
        else:
            self.redirect("/signup")
      
    def post(self):
        user_name = self.get_current_user()
        content = json.loads(self.request.get('ranking'))
        ranking_id, item_ids = database.add_new_ranking(content["title"], content["item_names"], content["item_contents"], user_name)
        database.update_ranking_history(ranking_id, user_name, item_ids)
        database.update_ranking_result(ranking_id, item_ids)
        time.sleep(0.2)
        self.redirect('/user/' + user_name)