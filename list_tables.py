import sqlite3
import os

db_path = r'c:\Users\harshal khedekar\OneDrive\Desktop\Mini Project(CSEDS) (3) 2\Mini Project(CSEDS)\instance\event_crowd.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")
    conn.close()
