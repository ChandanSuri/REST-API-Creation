from Models.user import User
from werkzeug.security import safe_str_cmp
# a safer way of comparing strings using safe_str_cmp due to diff formats

# not used now - begin
#users = [
#    User(1, "Chandan", "Chan21296")
#]

#username_mapping = {u.username: u for u in users}
#userid_mapping = {u.id: u for u in users}
# not used now - end


def authenticate(username, password):
    #changes after the sqlite connection, we don't use the in-memory mapping now
    user = User.find_by_username(username)
    #user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

# function specific to flask-jwt...
def identity(payload):
    user_id = payload["identity"]
    #changes after the sqlite connection, we don't use the in-memory mapping now
    return User.find_by_id(user_id)
    #return userid_mapping.get(user_id, None)
