import sqlite3

conn = sqlite3.connect("./utils/descriptions.sqlite3")
curr = conn.cursor()

def create_table(school_name):
    curr.execute(f"CREATE TABLE {school_name} (course_code TEXT, course_description TEXT, catoid TEXT, coid TEXT)")
    conn.commit()

def insert_into_db(school_name, course_code, course_description, catoid, coid):
    curr.execute(f"INSERT INTO {school_name} (course_code, course_description, catoid, coid) VALUES (?, ?, ?, ?)", (course_code, course_description, catoid, coid))
    conn.commit()
    print(f'{course_code} inserted')

def get_course_info(school_name, course_code):
    return curr.execute(f"SELECT * FROM {school_name} WHERE course_code=?", (course_code,)).fetchone()

def get_courses(school_name):
    return curr.execute(f"SELECT * FROM {school_name}").fetchall()
