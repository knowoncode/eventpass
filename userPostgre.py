from psycopg2 import connect
from flask import session
import os

# PostgreSQL configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "eventpass")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")


class User:

    def connection(self):

        con = connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )

        return con

    def userInsert(self, firstName, lastName, email, password):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            CREATE TABLE IF NOT EXISTS users(
                firstName VARCHAR(255),
                lastName VARCHAR(255),
                email VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255)
            )
        '''

        cur.execute(sq)

        # Check duplicate
        cur.execute(
            "SELECT 1 FROM users WHERE email=%s",
            (email,)
        )

        exist = cur.fetchone()

        if exist:
            db.close()
            return 1

        sq = '''
            INSERT INTO users(
                firstName,
                lastName,
                email,
                password
            )
            VALUES(%s, %s, %s, %s)
        '''

        record = [
            firstName,
            lastName,
            email,
            password
        ]

        cur.execute(sq, record)

        db.commit()
        db.close()

        return 0

    def userLogin(self, email, password):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            SELECT firstName, email
            FROM users
            WHERE email=%s AND password=%s
        '''

        value = [
            email,
            password
        ]

        cur.execute(sq, value)

        row = cur.fetchall()

        db.close()

        if row:

            session['userName'] = row[0][0]
            session['userEmail'] = row[0][1]

            return True

        else:
            return False

    def userProfile(self):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            SELECT firstName, lastName, email
            FROM users
            WHERE email=%s
        '''

        value = [
            session['userEmail']
        ]

        cur.execute(sq, value)

        row = cur.fetchone()

        db.close()

        return row

    def userProfileUpdate(self, firstName, lastName):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            UPDATE users
            SET
                firstName=%s,
                lastName=%s
            WHERE email=%s
        '''

        value = [
            firstName,
            lastName,
            session['userEmail']
        ]

        cur.execute(sq, value)

        db.commit()

        session['userName'] = firstName

        db.close()

    def deleteAccount(self):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            DELETE FROM users
            WHERE email=%s
        '''

        value = [
            session['userEmail']
        ]

        cur.execute(sq, value)

        db.commit()
        db.close()

    def changePassword(self, oldPassword, newPassword):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            SELECT 1
            FROM users
            WHERE email=%s AND password=%s
        '''

        value = [
            session['userEmail'],
            oldPassword
        ]

        cur.execute(sq, value)

        row = cur.fetchall()

        if row:

            sq = '''
                UPDATE users
                SET password=%s
                WHERE email=%s
            '''

            value = [
                newPassword,
                session['userEmail']
            ]

            cur.execute(sq, value)

            db.commit()
            db.close()

            return True

        else:

            db.close()

            return False

    def viewCollege(self):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            SELECT college, email
            FROM admin
        '''

        cur.execute(sq)

        row = cur.fetchall()

        db.close()

        return row

    def searchEvent(self, collegeEmail):

        db = self.connection()
        cur = db.cursor()

        # MySQL CURDATE() changed to PostgreSQL CURRENT_DATE
        sq = '''
            SELECT
                eventID,
                eventName,
                startDate,
                endDate,
                venue,
                capacity,
                type
            FROM event
            WHERE adminEmail=%s
            AND endDate >= CURRENT_DATE
        '''

        value = [collegeEmail]

        cur.execute(sq, value)

        row = cur.fetchall()

        db.close()

        return row

    def generatePass(self, eventID):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            SELECT
                eventID,
                eventName,
                startDate,
                endDate,
                type
            FROM event
            WHERE eventID=%s
        '''

        value = [eventID]

        cur.execute(sq, value)

        row = cur.fetchone()

        db.close()

        return row

    def eventPass(self, eventID, email, img):

        db = self.connection()
        cur = db.cursor()

        sq = '''
            CREATE TABLE IF NOT EXISTS eventPass(
                eventID INTEGER,
                email VARCHAR(255),
                img VARCHAR(255),
                PRIMARY KEY(eventID, email)
            )
        '''

        cur.execute(sq)

        # Check duplicate
        cur.execute(
            '''
            SELECT 1
            FROM eventPass
            WHERE email=%s AND eventID=%s
            ''',
            (email, eventID)
        )

        exist = cur.fetchone()

        if exist:

            db.close()

            return True

        sq = '''
            INSERT INTO eventPass(
                eventID,
                email,
                img
            )
            VALUES(%s, %s, %s)
        '''

        record = [
            eventID,
            email,
            img
        ]

        cur.execute(sq, record)

        db.commit()
        db.close()

        return 0