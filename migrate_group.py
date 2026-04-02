import sqlite3
import os

db_path = os.path.join('instance', 'event_crowd.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Adding group event columns...")
        
        # Add is_group_event to event table
        try:
            cursor.execute("ALTER TABLE event ADD COLUMN is_group_event BOOLEAN DEFAULT 0")
            print("Successfully added 'is_group_event' to 'event'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("'is_group_event' already exists.")
            else:
                raise e

        # Add guest_name to ticket table
        try:
            cursor.execute("ALTER TABLE ticket ADD COLUMN guest_name VARCHAR(100)")
            print("Successfully added 'guest_name' to 'ticket'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("'guest_name' already exists.")
            else:
                raise e
        
        conn.commit()
        conn.close()
        print("Group event migration completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
