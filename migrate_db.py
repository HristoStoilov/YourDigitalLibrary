"""
Database migration script to add role and is_banned columns to User table
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'library.db')

def migrate_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add role column if it doesn't exist
        if 'role' not in columns:
            print("Adding 'role' column to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'normal' NOT NULL")
            print("✓ 'role' column added successfully")
        else:
            print("✓ 'role' column already exists")
        
        # Add is_banned column if it doesn't exist
        if 'is_banned' not in columns:
            print("Adding 'is_banned' column to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_banned BOOLEAN DEFAULT 0 NOT NULL")
            print("✓ 'is_banned' column added successfully")
        else:
            print("✓ 'is_banned' column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please run the application first to create the database.")
    else:
        print("Starting database migration...\n")
        migrate_database()
