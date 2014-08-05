class Ranking(Entity):
    
    title = db.StringProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)
    creator = db.StringProperty(required = True)
    

def get_ranking_by_id(ranking_id):
    return Ranking.get_by_id(ranking_id)

def get_user_rankings(user_name):
    return Ranking.all().filter('creator =', user_name).order('-created').fetch(limit=100)
    
def get_recent_rankings():
    return Ranking.all().order('-created').fetch(limit=100)

def add_new_ranking(title, item_names, item_contents, creator):
    ranking = Ranking(creator=creator, title=title, created=datetime.datetime.now())
    ranking.put()
    item_ids = []
    for i in range(len(item_names)):
        item_ids.append(add_new_item(item_names[i], item_contents[i], creator))
    return ranking.get_id(), item_ids