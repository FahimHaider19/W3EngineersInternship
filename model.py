class UserModel(db.Model):
    __tablename__ = 'user'
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    # def save(self):
    #     self.id = 1