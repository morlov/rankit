import handler
import database

class MainPage(handler.Handler):

    def get(self):
        if self.get_current_user():
            self.render_main_page()
        else:
            self.redirect("/signup")

    def render_main_page(self):
        current_user_name = self.get_current_user()
        rankings = database.get_recent_rankings()
        items, is_sorted = {}, {}
        for r in rankings:
            rid = r.get_id()
            items[rid] = database.get_ranking_items(rid)
            is_sorted[rid] = database.is_ranking_sorted_by_user(rid, current_user_name)
        self.render("main.html", current_user_name=current_user_name, rankings=rankings, items=items, is_sorted=is_sorted)