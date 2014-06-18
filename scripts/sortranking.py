import handler
import json
import database

class SortRanking(handler.Handler):

    def get(self, ranking_id):
        ranking_id = int(ranking_id)
        ranking = database.get_ranking_by_id(ranking_id)
        if not ranking:
            self.error(404)
            return

        user_name = self.get_current_user()
        if user_name:
            items = database.get_ranking_items(ranking_id)
            self.render("sort.html", user_name=user_name, ranking=ranking, items=items)
        else:
            self.redirect("/signup")
      
    def post(self, ranking_id):
        
        current_user_name = self.get_current_user()
        
        if database.is_ranking_sorted_by_user(rid, current_user_name):
            self.redirect("/signup")

        ranking_id = int(ranking_id)
        user_name = self.get_current_user()
        content = json.loads(self.request.get('ranking'))
        item_ids = [int(i) for i in content["item_ids"]]

        database.update_ranking_history(ranking_id, user_name, item_ids)
        database.update_ranking_result(ranking_id, item_ids)
        self.redirect('/')
