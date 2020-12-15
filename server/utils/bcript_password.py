import bcrypt

class Bcript_password():
    def hash(password):
        salt = bcrypt.gensalt()
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hashed
    def compare(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
