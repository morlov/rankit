import datetime
from google.appengine.ext import db


# Objects used in the app
class Entity(db.Model):

    def get_id(self):
        return int(self.key().id())

class User(Entity):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = True)

def get_user_by_name(user_name):
    return db.GqlQuery("SELECT * FROM User WHERE name=:name", name=user_name).get()

def get_user_by_email(email):
    return db.GqlQuery("SELECT * FROM User WHERE email=:email",email=email).get()

def add_new_user(user_name, password, email):
    user = User(name=user_name, password=password, email=email)
    user.put()
    return user.get_id()
 
class Item(Entity):
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

def add_new_item(name, content, creator):
    item = Item(name=name, content=content, creator=creator)
    item.put()
    return item.get_id()

class Ranking(Entity):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    creator = db.StringProperty(required = True)

def get_ranking_by_id(ranking_id):
    return Ranking.get_by_id(ranking_id)

def get_user_rankings(user_name):
    return db.GqlQuery("select * from Ranking where creator=:user_name order by created desc limit 100", user_name=user_name)

def get_recent_rankings():
    return db.GqlQuery("select * from Ranking order by created desc limit 100")

def is_ranking_sorted_by_user(ranking_id, user_name):
    return db.GqlQuery("select * from RankingHistory where user = :user_name and ranking_id=:ranking_id", user_name=user_name, ranking_id=ranking_id).get() is not None

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

def update_ranking_history(ranking_id, user_name, item_ids):
    date=datetime.datetime.now()
    for i in item_ids:
        RankingHistory(ranking_id=ranking_id, user=user_name, item_id=i, date=date, rank=item_ids.index(i) + 1).put()

class RankingResult(Entity):
    ranking_id = db.IntegerProperty(required = True)
    item_id = db.IntegerProperty(required = True)
    borda_count = db.IntegerProperty(required = True)

def get_ranking_items(ranking_id):
    # results = db.GqlQuery("select * from RankingResult where ranking_id=:ranking_id order by borda_count desc", ranking_id=ranking_id)
    print type(ranking_id)
    results = RankingResult.all().filter("ranking_id=",ranking_id)
    print results
    item_ids = [res for res in results]
    print item_ids
    return Item.get_by_id(item_ids)

def get_borda_counts(ranking_id, item_ids):
    borda_counts = []
    for i in item_ids:
        result = RankingResult.all().filter("ranking_id=",ranking_id).filter("item_id=",i).get()
        # result = db.GqlQuery("select * from RankingResult where ranking_id=:ranking_id and item_id=:item_id", ranking_id=ranking_id, item_id=i)
        borda_counts.append(result.borda_count)
    return borda_counts

def set_borda_counts(ranking_id, item_ids, new_borda_counts):
    for z in zip(item_ids, new_borda_counts):
        result = db.GqlQuery("select * from RankingResult where ranking_id=:ranking_id and item_id=:item_id", ranking_id=ranking_id, item_id=z[0])
        if not result.get():
            RankingResult(ranking_id=ranking_id, item_id = z[0], borda_count = z[1]).put()
        else:
            for r in result:
                r.borda_count = z[1]
                r.put()
# TODO: on updating ranking ranking is already added and 
def update_ranking_result(ranking_id, item_ids):
    if RankingResult.all().filter('ranking_id', ranking_id).get():
        old_borda_counts = get_borda_counts(ranking_id, item_ids)
        new_borda_counts = borda_count(item_ids, old_borda_counts)
    else:
        new_borda_counts = borda_count(item_ids)
    set_borda_counts(ranking_id, item_ids, new_borda_counts)

def borda_count(item_ids, old_borda_counts=None):
    new_borda_counts = range(len(item_ids), 0,-1)
    if old_borda_counts:
        new_borda_counts = map(lambda x,y: x+y, old_borda_counts, new_borda_counts)
    return new_borda_counts


