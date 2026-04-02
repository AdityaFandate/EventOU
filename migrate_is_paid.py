import sqlite3
import os

# Use absolute path for safety
db_path = r"c:\Users\harshal khedekar\OneDrive\Desktop\Mini Project(CSEDS) (3) 2\Mini Project(CSEDS)\instance\event_crowd.db"

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Found tables: {tables}")
        
        if 'event' not in tables:
            print("Table 'event' not found. This might mean the DB is not initialized yet.")
            print("Please run the app once to initialize the DB, then run this migration.")
        else:
            # Add is_paid to event
            print("Adding 'is_paid' column to 'event'...")
            try:
                cursor.execute("ALTER TABLE event ADD COLUMN is_paid BOOLEAN DEFAULT 0")
                print("Successfully added 'is_paid'.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("'is_paid' already exists.")
                else:
                    raise e

            # Add price to event
            print("Adding 'price' column to 'event'...")
            try:
                cursor.execute("ALTER TABLE event ADD COLUMN price FLOAT DEFAULT 0.0")
                print("Successfully added 'price'.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("'price' already exists.")
                else:
                    raise e

            # Add is_group_event to event
            print("Adding 'is_group_event' column to 'event'...")
            try:
                cursor.execute("ALTER TABLE event ADD COLUMN is_group_event BOOLEAN DEFAULT 0")
                print("Successfully added 'is_group_event'.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("'is_group_event' already exists.")
                else:
                    raise e
        
        conn.commit()
        conn.close()
        print("Migration process finished.")
    except Exception as e:
        print(f"An error occurred: {e}")
