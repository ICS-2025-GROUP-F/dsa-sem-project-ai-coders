import sqlite3
import os

def get_db_connection():
    """
    Returns a connection to the SQLite database.
    Creates the database and tables if they don't exist.
    """
    # Get the directory of the current file
    db_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the database path to be in the data directory
    db_path = os.path.join(db_dir, 'student_db.sqlite')
    
    # Connect to SQLite database (will create if it doesn't exist)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Create tables if they don't exist
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            math REAL,
            science REAL,
            english REAL
        )
    ''')
    conn.commit()
    
    return conn
