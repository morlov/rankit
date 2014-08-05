"""

This class implements user of rankit web service.

"""


class User(Entity):
	
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = True)

	def get_user_by_name(user_name):
    	return User.all().filter("name =", user_name).get()

	def get_user_by_email(email):
    	return User.all().filter("email =",email).get()

	def save_user(user_name, password, email):
    	user = User(name=user_name, password=password, email=email)
    	user.put()
    	return user.get_id()