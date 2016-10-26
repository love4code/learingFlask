from ..app import Role, User, db
# These were examples from the book on working with the db from the terminal

#  Modifying Rows
# The add() Method  of the database session can also be used to update
# models
admin_role.name = 'Administrator'
db.session.add(admin_role)
# >>> print(str(admin_role))
# <Role 'Administrator'>
db.session.commit()

# Deleting Rows

db.session.delete(mod_role)
db.session.commit()

# Querying Rows

User.query.all()
#  [<User 'John'>, <User 'Susan'>, <User 'David'>]

User.query.filter_by(role=user_role).all()
# AttributeError: 'str' object has no attribute '_sa_instance_state'
# >>> from TestApp.DB_Opperations.insertingRows import user_role
# >>> User.query.filter_by(role=user_role).all()
# [<User 'Susan'>, <User 'David'>]

str(User.query.filter_by(role=user_role))
# 'SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id \nFROM users \nWHERE ? = users.role_id'
