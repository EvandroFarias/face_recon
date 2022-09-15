import numpy as np
import psycopg2

class DatabaseManagement:

    _db = None

    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(host=mhost, database=db, user=usr, password=pwd)

    def create_initial_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS face_owner(
            id SERIAL, name VARCHAR, PRIMARY KEY (id));
        CREATE TABLE IF NOT EXISTS encoding (
            owner BIGINT references face_owner(id),
            encoded_face VARCHAR);
            """

        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()

        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"

    def insert_owner(self, name: str):
        sql = f"insert into face_owner (name) values('{name}')"
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()

        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"

    def insert_face(self, owner: int, encode: str):
        sql = f"""
        insert into encoding (owner, encoded_face) values({owner}, '{encode}')
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"

    def select_owner_by_face_encode(self, encode: str):
        sql = f"""
        select f.id from face_owner f JOIN encoding e ON e.owner = f.id where e.encoded_face = '{encode}'
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            fetch = cur.fetchall()
            print(fetch[0][0])
            cur.close()
            self._db.commit()
            return fetch[0][0]
        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"

    def select_owner_by_name(self, owner):
        sql = f"""
        select id from face_owner where name = '{owner}'
        """
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            fetch = cur.fetchall()
            cur.close()
            self._db.commit()
            return fetch[0][0]
        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"

    def select_all_faces(self):
        sql = "select * from encoding"
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            fetch = cur.fetchall()
            for id, face in fetch:
                print(f"")
            cur.close()
            self._db.commit()
            return {id, face}
        except(Exception, psycopg2.DatabaseError) as ex:
            return f"Some error occurred {ex}"