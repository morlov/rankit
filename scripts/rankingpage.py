import handler
import json
import database

class RankingPage(handler.Handler):

    def get(self, ranking_id):
        ranking_id = int(ranking_id)
        ranking = database.get_ranking_by_id(ranking_id)
        if not ranking:
            self.error(404)
            return

        current_user_name = self.get_current_user()
        if current_user_name:
            items = database.get_ranking_items(ranking_id)
            is_sorted = database.is_ranking_sorted_by_user(ranking_id, current_user_name)
            self.render("ranking.html", current_user_name=current_user_name, ranking=ranking, items=items, is_sorted=is_sorted)
        else:
            self.redirect("/signup")
      
    def post(self, ranking_id):
        
        ranking_id = int(ranking_id)
        current_user_name = self.get_current_user()
        
        if database.is_ranking_sorted_by_user(ranking_id, current_user_name):
            self.response.out.write('You have already submitted this ranking!')
            return

        user_name = self.get_current_user()
        content = json.loads(self.request.get('ranking'))
        item_ids = [int(i) for i in content["item_ids"]]

        database.update_ranking_history(ranking_id, user_name, item_ids)
        database.update_ranking_result(ranking_id, item_ids)
        self.redirect('/ranking/'+str(ranking_id))