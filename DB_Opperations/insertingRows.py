from ..app import Role, User, db
# These were examples from the book on working with the db from the terminal

admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='John', role=admin_role)
user_susan = User(username='Susan', role=user_role)
user_david = User(username='David', role=user_role)

print("Before: ",admin_role.id)
print("Before: ",user_role.id)
print("Before: ",mod_role.id)


db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)

print("After: ",admin_role.id)
print("After: ",user_role.id)
print("After: ",mod_role.id)
