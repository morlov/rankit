import handler
import database

class UserPage(handler.Handler):

    def get(self, user_name):

        if not database.get_user_by_name(user_name):
            self.error(404)

        if self.get_current_user():
            self.render_user_page(user_name)
        else:
            self.redirect("/signup")
        

    def render_user_page(self, user_name):
        current_user_name = self.get_current_user()
        rankings = database.get_user_rankings(user_name)
        items, is_sorted = {}, {}
        for r in rankings:
            rid = r.get_id()
            items[rid] = database.get_ranking_items(rid)
            is_sorted[rid] = database.is_ranking_sorted_by_user(rid, current_user_name)
        self.render("user.html", current_user_name=current_user_name, user_name=user_name, rankings=rankings, items=items, is_sorted=is_sorted)
