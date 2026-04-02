import sqlite3
import os

db_path = os.path.join('instance', 'event_crowd.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Adding 'coupon_id' column to 'food_coupon_redemption'...")
        try:
            cursor.execute("ALTER TABLE food_coupon_redemption ADD COLUMN coupon_id INTEGER REFERENCES food_coupon(id)")
            print("Successfully added 'coupon_id'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("'coupon_id' already exists.")
            else:
                raise e

        print("Adding 'event_id' column to 'food_coupon_redemption'...")
        try:
            cursor.execute("ALTER TABLE food_coupon_redemption ADD COLUMN event_id INTEGER REFERENCES event(id)")
            print("Successfully added 'event_id'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("'event_id' already exists.")
            else:
                raise e
        
        conn.commit()
        conn.close()
        print("Migration completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
