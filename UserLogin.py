class UserLogin():

    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

    def getStyleID(self):
        return self.__user['styleID'] if self.__user else 'User not found'

    def verifyExt(self, filename):
        ext = filename.split('.', 1)[1]
        if ext.lower() in ('jpg', 'jpeg'):
            return True
        return False