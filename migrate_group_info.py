import sqlite3
import os

db_path = os.path.join('instance', 'event_crowd.db')

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Migrating database to add team_name and member_details to ticket table...")
    
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN team_name VARCHAR(100)")
        print("Added column team_name")
    except sqlite3.OperationalError:
        print("Column team_name already exists")
        
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN member_details TEXT")
        print("Added column member_details")
    except sqlite3.OperationalError:
        print("Column member_details already exists")
        
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
