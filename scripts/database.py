import datetime
from google.appengine.ext import db

class Entity(db.Model):

    def get_id(self):
        return self.key().id()

class User(Entity):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = True)

def get_user_by_name(user_name):
    return User.all().filter('name =', user_name).get()

def get_user_by_email(email):
    return User.all().filter("email =",email).get()

def add_new_user(user_name, password, email):
    user = User(name=user_name, password=password, email=email)
    user.put()
    return user.get_id()
 
class Item(Entity):
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = False)
    content = db.TextProperty(required = False)

def add_new_item(name, content, creator):
    item = Item(name=name, content=content, creator=creator)
    item.put()
    return item.get_id()

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
        
class RankingHistory(Entity):
    ranking_id = db.IntegerProperty(required = True)
    user = db.StringProperty(required = True)
    item_id = db.IntegerProperty(required = True)
    rank = db.IntegerProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

def is_ranking_sorted_by_user(ranking_id, user_name):
    return RankingHistory.all().filter('user =',user_name).filter('ranking_id =', ranking_id).get() is not None

def update_ranking_history(ranking_id, user_name, item_ids):
    date=datetime.datetime.now()
    for i in item_ids:
        RankingHistory(ranking_id=ranking_id, user=user_name, item_id=i, date=date, rank=item_ids.index(i) + 1).put()

class RankingResult(Entity):
    ranking_id = db.IntegerProperty(required = True)
    item_id = db.IntegerProperty(required = True)
    borda_count = db.IntegerProperty(required = True)

def get_ranking_items(ranking_id):
    result = RankingResult.all().filter('ranking_id =', ranking_id)
    result.order('-borda_count')
    return Item.get_by_id([r.item_id for r in result])

def update_ranking_result(ranking_id, item_ids):
    result = RankingResult.all().filter('ranking_id =', ranking_id)
    item_count = {r.item_id:r.borda_count for r in result}
    old_borda_counts = [item_count[i] for i in item_ids]
    new_borda_counts = borda_count(item_ids, old_borda_counts)
    item_count = dict(zip(item_ids, new_borda_counts))
    for r in result:
        r.borda_count = item_count[r.item_id]
        r.put()

def init_ranking_result(ranking_id, item_ids):
    new_borda_counts = borda_count(item_ids)
    for (i, b) in zip(item_ids, new_borda_counts):
        RankingResult(ranking_id=ranking_id, item_id=i, borda_count=b).put()

def borda_count(item_ids, old_borda_counts=None):
    new_borda_counts = range(len(item_ids), 0,-1)
    if old_borda_counts:
        new_borda_counts = map(lambda x,y: x+y, old_borda_counts, new_borda_counts)
    return new_borda_counts


