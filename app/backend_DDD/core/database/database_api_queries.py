import os
import json
import psycopg2
import datetime
from dotenv import load_dotenv, find_dotenv
from app.backend_DDD.core.scripts import pdc_extract_menu_script as pdc_script

load_dotenv(find_dotenv())

class DatabaseManager:
    def __init__(self, admin=None, scripts=None):
        self.database_url = os.environ.get('HEROKU_POSTGRESQL_CYAN_URL')
        self.conn = None
        self.cursor = None
        self.retryConnect = 3
        self.connect()
        # Set the Admin instance after initialization
        self.admin = admin if admin else Admin(self)
        self.scripts = scripts if scripts else Scripts(self)

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



    def insert_user(self, user_name: str, uid: str, email: str):
        sql_insert_1 = """INSERT INTO users (user_id, user_name, user_email, affiliate_id, user_type) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"""
        try:
            self.cursor.execute(sql_insert_1, (uid,user_name, email, "1", "user"))
            user_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"User {user_name} inserted with user_id: {user_id}")
            return user_id
        except Exception as e:
            print(f"Error inserting user: {e}")
            self.conn.rollback()
            return None
    
    def set_new_user_details(self, user_id: str):
        sql_insert_2 = """
            INSERT INTO user_profile_setup (user_id, university_set_up, courses_set_up, email_verified)
            VALUES (%s, %s, %s, %s);
        """
        try:
            # Only three boolean values are required after user_id
            self.cursor.execute(sql_insert_2, (user_id, False, False, False))
            self.conn.commit()
            print(f"User details inserted for user {user_id}.")
        except Exception as e:
            print(f"Error inserting user details: {e}")
            self.conn.rollback()
        
    def create_user(self, user_name: str, uid: str, email: str):
        user_id = self.insert_user(user_name, uid, email)
        if user_id:
            self.set_new_user_details(user_id)
            return user_id
        else:
            return None
        
    def get_user_id(self, user_id: int):
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
        
    def get_user(self, user_id: str):
        try:
            # Select user_name, user_email, and user_type for the given user_id
            self.cursor.execute(
                "SELECT user_name, user_email, user_type FROM users WHERE user_id = %s", 
                (user_id,)
            )
            user = self.cursor.fetchone()

            if user:
                # Return user details as a dictionary
                return {
                    'uid' : user_id,
                    'user_name': user[0],
                    'user_email': user[1],
                    'user_type': user[2]
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting user from database: {e}")
            return None
        
    def get_user_setup(self, user_id: str):
        try:
            # Select user_name, user_email, and user_type for the given user_id
            self.cursor.execute(
                "SELECT university_set_up, courses_set_up, email_verified FROM user_profile_setup WHERE user_id = %s", 
                (user_id,)
            )
            user_setup = self.cursor.fetchone()

            if user_setup:
                # Return user details as a dictionary
                return {
                    'university_set_up': user_setup[0],
                    'courses_set_up': user_setup[1],
                    'email_verified': user_setup[2]
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting user setup from database: {e}")
            return None
        
    def get_assistant_id_by_name(self, assistant_name: str):
        self.cursor.execute("SELECT assistant_id FROM assistant_details WHERE assistant_name = %s", (assistant_name,))
        assistant_id = self.cursor.fetchone()
        if assistant_id:
            return assistant_id[0]
        else:
            return None
        
    def set_thread_id(self, user_id: str, thread_id: str):
        sql_insert_3 = """INSERT INTO user_threads (user_id, thread_id, thread_name) VALUES (%s, %s, %s);"""
        try:
            self.cursor.execute(sql_insert_3, (user_id, thread_id, ''))
            self.conn.commit()
            print(f"Thread ID {thread_id} inserted for user {user_id}.")
        except Exception as e:
            print(f"Error inserting thread ID: {e}")
            self.conn.rollback()
        
        

    def get_university_setup(self):
        setup = {}
        self.cursor.execute("SELECT university_id, university_name FROM university;")
        universities = self.cursor.fetchone()
        setup['university'] = {
            'id': universities[0],
            'name': universities[1]
        }

        self.cursor.execute("SELECT university_school_id, majors_list, school_name, school_name_abv, university_school_regex FROM university_school WHERE university_id = %s", (setup['university']['id'],))
        schools = self.cursor.fetchall()
        setup['schools'] = [{'id': school[0], 'majors_list': school[1], 'school_name': school[2], 'school_name_abv': school[3], 'regex': school[4]} for school in schools]
        self.cursor.execute("SELECT affiliate_id, affiliate_type, affiliate_email_regex FROM affiliate_details WHERE university_id = %s", (str(setup['university']['id']),))
        affiliates = self.cursor.fetchall()
        setup['affiliates'] = [{'id': affiliate[0], 'type': affiliate[1], 'regex': affiliate[2]} for affiliate in affiliates]
        return setup
        
    def set_university_setup(self, user_id: str, email: str, affiliation: str, school_id: int, major: str, graduation_year: int):
        sql_insert = """
        INSERT INTO student_details 
        (user_id, university_id, university_linked_email, university_school_id, major, expected_graduation_year, email_otp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        sql_update = """
        UPDATE user_profile_setup
        SET university_set_up = %s
        WHERE user_id = %s;
        """

        sql_update_2 = """
        UPDATE users
        SET affiliate_id = %s
        WHERE user_id = %s;
        """

        sql_check = """ 
        SELECT university_set_up FROM user_profile_setup WHERE user_id = %s;
        """
        
        # Assuming email_otp is a randomly generated number for this example
        import random
        email_otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
    
        try:
            # Check if the user has already set up university details
            self.cursor.execute(sql_check, (user_id,))
            university_set_up = self.cursor.fetchone()[0]
            if university_set_up:
                print(f"University details already set up for user {user_id}.")
                return

            # Execute the SQL command with fixed university_id set to 1
            self.cursor.execute(sql_insert, (user_id, 1, email, school_id, major, graduation_year, email_otp))
            self.cursor.execute(sql_update, (True, user_id))
            self.cursor.execute(sql_update_2, (affiliation, user_id))
            self.conn.commit()
            print(f"Student details inserted for user {user_id}.")
        except Exception as e:
            print(f"Error inserting student details: {e}")
            self.conn.rollback()


    def skip_set_university_setup(self, user_id: str,):

        sql_update = """
        UPDATE user_profile_setup
        SET university_set_up = %s
        WHERE user_id = %s;
        """

        sql_update_2 = """
        UPDATE users
        SET affiliate_id = %s
        WHERE user_id = %s;
        """

        sql_check = """ 
        SELECT university_set_up FROM user_profile_setup WHERE user_id = %s;
        """
        
    
        try:
            # Check if the user has already set up university details
            self.cursor.execute(sql_check, (user_id,))
            university_set_up = self.cursor.fetchone()[0]
            if university_set_up:
                print(f"University details already set up for user {user_id}.")
                return

            # Execute the SQL command with fixed university_id set to 1
            self.cursor.execute(sql_update, (True, user_id))
            self.cursor.execute(sql_update_2, ('1', user_id))
            self.conn.commit()
            print(f"Student details inserted for user {user_id}.")
        except Exception as e:
            print(f"Error inserting student details: {e}")
            self.conn.rollback()
        
    def insert_user_threads(self, user_id: str, thread_id: str, thread_name: str):
        sql_insert_2 = """
            INSERT INTO user_threads (user_id, thread_id, thread_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (thread_id)
            DO UPDATE SET thread_name = EXCLUDED.thread_name;
        """
        try:
            # Execute the insert or update query
            self.cursor.execute(sql_insert_2, (user_id, thread_id, thread_name))
            self.conn.commit()
            print(f"User thread inserted or updated for user {user_id}.")
        except Exception as e:
            print(f"Error inserting or updating user threads: {e}")
            self.conn.rollback()

    def get_threads(self, user_id: int) -> list:
        try:
            # Fetch both thread_id and thread_name from the user_threads table
            self.cursor.execute("SELECT thread_id, thread_name, thread_updated_at FROM user_threads WHERE user_id = %s", (user_id,))
            threads = self.cursor.fetchall()

            # If threads are found, return a list of dictionaries with id and name
            if threads:
                return [{'id': thread[0], 'name': thread[1], 'updated_at' : thread[2]} for thread in threads]
            else:
                return []
        except Exception as e:
            print(f"Error getting threads from database: {e}")
            return []
        
    def updated_thread_time(self, thread_id: str):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql_update = """
        UPDATE user_threads
        SET thread_updated_at = %s
        WHERE thread_id = %s;
        """
        try:
            self.cursor.execute(sql_update, (current_time,thread_id,))
            self.conn.commit()
            print(f"Thread {thread_id} updated.")
        except Exception as e:
            print(f"Error updating thread: {e}")
            self.conn.rollback()



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

    def get_pdc_eateries(self):
        """
        Fetch all data from the database in three queries and format it into the original JSON-like dictionary structure.
        Returns:
            dict: Data structured as per the original JSON format.
        """
    
        try:
            # Fetch all eateries
            self.cursor.execute("SELECT * FROM pdc_eateries")
            eateries = self.cursor.fetchall()
    
            # Fetch all menu items
            self.cursor.execute("SELECT * FROM pdc_menu_items")
            menu_items = self.cursor.fetchall()
    
            # Fetch all prices
            self.cursor.execute("SELECT * FROM pdc_menu_prices")
            prices = self.cursor.fetchall()
    
            # Organize data
            result = []
            eatery_dict = {eatery[0]: {"name": eatery[1], "link": eatery[2], "menu": []} for eatery in eateries}
            menu_item_dict = {}
    
            # Organize menu items under eateries
            for item in menu_items:
                item_id = item[0]
                eatery_id = item[1]
                item_data = {
                    "name": item[2],
                    "image_link": item[3],
                    "price": {}
                }
                menu_item_dict[item_id] = item_data
                eatery_dict[eatery_id]["menu"].append(item_data)
    
            # Organize prices under menu items
            for price in prices:
                menu_item_id = price[1]
                price_type = price[2]
                price_value = str(price[3]) if price[3] else ""
                if menu_item_id in menu_item_dict:
                    menu_item_dict[menu_item_id]["price"][price_type] = price_value
    
            # Convert to result format
            for eatery in eatery_dict.values():
                result.append({
                    "eatery": eatery["name"],
                    "link": eatery["link"],
                    "menu": eatery["menu"]
                })
    
            return result
    
        except Exception as e:
            raise Exception(f"Error fetching or processing data: {e}")
    
    


    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed.")


class Scripts:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Store the DatabaseManager instance for access
        super().__init__()

    def update_pdc_menu(self, pdc_menu_data: dict):
        try:

            pdc_script.clear_data(self.db_manager.cursor)

            data = pdc_menu_data

            # Insert eateries and their related data
            for eatery in data:
                eatery_id = pdc_script.insert_eatery(self.db_manager.cursor, eatery["eatery"], eatery["link"], eatery["image"])
                # print(f"Inserted Eatery: {eatery['eatery']} with ID {eatery_id}")

                # Insert menu items
                for item in eatery["menu"]:
                    menu_item_id = pdc_script.insert_menu_item(self.db_manager.cursor, eatery_id, item["name"], item["image_link"])
                    # print(f"Inserted Menu Item: {item['name']} with ID {menu_item_id}")

                    # Insert prices
                    for price_type, price_value in item["price"].items():
                        if price_value:  # Only insert non-empty prices
                            pdc_script.insert_price(self.db_manager.cursor, menu_item_id, price_type, price_value)
                            # print(f"Inserted Price: {price_type} - {price_value} for Menu Item ID {menu_item_id}")

            # Commit the transaction
            self.db_manager.conn.commit()
            print("Data inserted successfully.")

        except Exception as e:
            print(f"Error while inserting data: {e}")
            self.db_manager.conn.rollback()



class Admin:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Store the DatabaseManager instance for access
        super().__init__()


    def view_all_users(self):
        sql_select_all_users = "SELECT user_id, user_name FROM users;"
        try:
            self.db_manager.cursor.execute(sql_select_all_users)
            users = self.db_manager.cursor.fetchall()
            return [{'user_id': user[0], 'user_name': user[1]} for user in users]
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []

    def view_all_universities(self):
        sql_select_all_universities = "SELECT university_id, university_name FROM universities;"
        try:
            self.db_manager.cursor.execute(sql_select_all_universities)
            universities = self.db_manager.cursor.fetchall()
            return [{'university_id': university[0], 'university_name': university[1]} for university in universities]
        except Exception as e:
            print(f"Error retrieving universities: {e}")
            return []
    
    def add_university(self, university_name: str, email_regex: str, assistant_id: int):
        sql_insert_university = """INSERT INTO university (university_name, email_regex, university_assistant_id) VALUES (%s, %s, %s) RETURNING university_id;"""
        try:
            self.db_manager.cursor.execute(sql_insert_university, (university_name, email_regex, assistant_id))
            university_id = self.db_manager.cursor.fetchone()[0]
            self.db_manager.conn.commit()
            print(f"University {university_name} inserted with university_id: {university_id}")
            return university_id
        except Exception as e:
            print(f"Error inserting university: {e}")
            self.db_manager.conn.rollback()
            return None
        
    def delete_university(self, university_id: int):
        sql_delete_university = "DELETE FROM university WHERE university_id = %s;"
        try:
            self.db_manager.cursor.execute(sql_delete_university, (university_id,))
            self.db_manager.conn.commit()
            print(f"University {university_id} deleted.")
        except Exception as e:
            print(f"Error deleting university: {e}")
            self.db_manager.conn.rollback()

    def update_university(self, university_id: int, university_name: str, email_regex: str, assistant_id: int):
        sql_update_university = """UPDATE university SET university_name = %s, email_regex = %s, university_assistant_id = %s WHERE university_id = %s;"""
        try:
            self.db_manager.cursor.execute(sql_update_university, (university_name, email_regex, assistant_id, university_id))
            self.db_manager.conn.commit()
            print(f"University {university_id} updated.")
        except Exception as e:
            print(f"Error updating university: {e}")
            self.db_manager.conn.rollback()

    def add_school_data(self, university_id: str, school_name: str, majors_list: list[str], school_name_abv: str):
        sql_insert_school = """INSERT INTO university_school (university_id , majors_list, school_name, school_name_abv) VALUES (%s, %s, %s, %s) RETURNING university_school_id;"""
        try:
            self.db_manager.cursor.execute(sql_insert_school, (university_id , majors_list, school_name, school_name_abv))
            school_id = self.db_manager.cursor.fetchone()[0]
            self.db_manager.conn.commit()
            print(f"School {school_name} inserted with school_id: {school_id}")
            return school_id
        except Exception as e:
            print(f"Error inserting school: {e}")
            self.db_manager.conn.rollback()
            return None

    def view_all_assistants(self):
        sql_select_all_assistants = "SELECT assistant_id, assistant_name FROM assistants;"
        try:
            self.db_manager.cursor.execute(sql_select_all_assistants)
            assistants = self.db_manager.cursor.fetchall()
            return [{'assistant_id': assistant[0], 'assistant_name': assistant[1]} for assistant in assistants]
        except Exception as e:
            print(f"Error retrieving assistants: {e}")
            return
        
    def add_assistant(self, assistant_id: str, assistant_name: str):
        sql_insert_assistant = """INSERT INTO assistant_details (assistant_id, assistant_name) VALUES (%s, %s) RETURNING assistant_id;"""
        try:
            self.db_manager.cursor.execute(sql_insert_assistant, (assistant_id, assistant_name))
            assistant_id = self.db_manager.cursor.fetchone()[0]
            self.db_manager.conn.commit()
            print(f"Assistant {assistant_name} inserted with assistant_id: {assistant_id}")
            return assistant_id
        except Exception as e:
            print(f"Error inserting assistant: {e}")
            self.db_manager.conn.rollback()
            return None
        




