"""

This class implements item.

"""

class Item(Entity):
    
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = False)
    content = db.TextProperty(required = False)

	def save_item(name, content, creator):
    	item = Item(name=name, content=content, creator=creator)
    	item.put()
    	return item.get_id()