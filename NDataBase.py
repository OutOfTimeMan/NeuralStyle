import sqlite3
import time
import math
import re
from flask import url_for


class NDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, NULL, ?, NULL)", (email, hpsw, 1))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД' + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False

            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД' +str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False

            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД' +str(e))

        return False

    def updateUserImage(self, image, user_id):
        if not image:
            return False

        try:
            binary = sqlite3.Binary(image)
            tm = math.floor(time.time())
            self.__cur.execute(f"UPDATE users SET image = ?, time = ? WHERE id = ?", (binary, tm, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def updateUserStyleImageId(self, id, user_id):
        if not id:
            return False

        try:
            self.__cur.execute(f'UPDATE users SET styleID = ? WHERE id = ?', (id, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления styleID в БД: " + str(e))
            return False
        return True

