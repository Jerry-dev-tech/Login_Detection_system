import sqlite3

connection = sqlite3.connect("login_system.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

password TEXT

)
""")

cursor.execute("SELECT * FROM admin")

admin = cursor.fetchone()

if admin is None:

    cursor.execute(
        """
        INSERT INTO admin(username,password)
        VALUES(?,?)
        """,

        ("admin","admin123")

    )

connection.commit()

connection.close()

print("Database Created Successfully")