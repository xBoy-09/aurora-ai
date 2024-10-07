import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DatabaseManager:
    def __init__(self):
        self.database_url = os.environ.get('HEROKU_POSTGRESQL_CYAN_URL')
        self.conn = None
        self.cursor = None
        self.retryConnect = 3
        self.connect()

    def connect(self):
        attempt = 0
        while attempt < self.retryConnect:
            try:
                self.conn = psycopg2.connect(self.database_url, connect_timeout=10)
                self.cursor = self.conn.cursor()
                print("Connection successful.")
                return  # Exit once connected successfully
            except Exception as e:
                attempt += 1
                print(f"Error connecting to database (attempt {attempt}/{self.retryConnect}): {e}")
                if attempt == self.retryConnect:
                    raise Exception(f"Failed to connect to database after {self.retryConnect} attempts.")

    def create_tables(self):
        sql_create_1 = """
            CREATE TABLE IF NOT EXISTS user_threads (
                user_id INT REFERENCES users(user_id),
                thread_ids INT[] NOT NULL,
                PRIMARY KEY (user_id)
            );
        """
        sql_create_2 = """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                user_name VARCHAR(100) NOT NULL
            );
        """
        try:
            self.cursor.execute(sql_create_2)  # Create the 'users' table first
            self.cursor.execute(sql_create_1)  # Then create 'user_threads'
            self.conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    def insert_user(self, user_name: str, uid: str):
        sql_insert_1 = """INSERT INTO users (user_id, user_name) VALUES (%s, %s) RETURNING user_id;"""
        try:
            self.cursor.execute(sql_insert_1, (uid,user_name))
            user_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"User {user_name} inserted with user_id: {user_id}")
            return user_id
        except Exception as e:
            print(f"Error inserting user: {e}")
            self.conn.rollback()
            return None
        
    def create_user(self, user_name: str, uid: str):
        user_id = self.insert_user(user_name, uid)
        if user_id:
            self.insert_user_threads(user_id)
            return user_id
        else:
            return None
        
    def get_user(self, user_id: int):
        try:
            self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            user_id = self.cursor.fetchone()
            if user_id:
                return user_id[0]
            else:
                return None
        except Exception as e:
            print(f"Error getting user from database: {e}")
            return None
        
    def insert_user_threads(self, user_id: int):
        sql_insert_2 = """INSERT INTO user_threads (user_id, thread_ids) VALUES (%s, %s);"""
        try:
            self.cursor.execute(sql_insert_2, (user_id, []))
            self.conn.commit()
            print(f"User threads inserted for user {user_id}.")
        except Exception as e:
            print(f"Error inserting user threads: {e}")
            self.conn.rollback()

    def get_threads(self, user_id: int) -> list:
        try:
            # Fetch both thread_id and thread_name from the user_threads table
            self.cursor.execute("SELECT thread_id, thread_name FROM user_threads WHERE user_id = %s", (user_id,))
            threads = self.cursor.fetchall()

            # If threads are found, return a list of dictionaries with id and name
            if threads:
                return [{'id': thread[0], 'name': thread[1]} for thread in threads]
            else:
                return []
        except Exception as e:
            print(f"Error getting threads from database: {e}")
            return []



    def add_thread(self, user_id: int, thread_id: int):
        # Get the current thread_ids for the user
        threads = self.get_threads(user_id)
        
        # If threads exist, append the new thread_id, otherwise create a new list
        if threads:
            # if thread_id already exists, return
            if thread_id in threads:
                print(f"Thread {thread_id} already exists for user {user_id}.")
                return
            # TODO: Throw Exception
            threads.append(thread_id)
        else:
            threads = [thread_id]
        
        try:
            # Update the user_threads table with the new list of thread_ids
            self.cursor.execute(
                "UPDATE user_threads SET thread_ids = %s WHERE user_id = %s", 
                (threads, user_id)
            )
            self.conn.commit()
            print(f"Thread {thread_id} added for user {user_id}.")
        except Exception as e:
            print(f"Error adding thread {thread_id} for user {user_id}: {e}")
            self.conn.rollback()



    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed.")

