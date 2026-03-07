import sqlite3
# creates or opens usage.db file where everything is stored
conn = sqlite3.connect("usage.db")
# this is some bullshit to make the table actually usable
cursor = conn.cursor()
# checks if the table exists if not creates it
def setup():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage (
            item  TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)

    # loop for inserting shit in
    for item in [
        #glups
        "glup_emoji", "glup_gif", "glup_sticker",
        #steamhappy
        "steamhappy_emoji", "steamhappy_gif"
        ]:
        cursor.execute(
        "INSERT OR IGNORE INTO usage (item, count) VALUES (?, 0)",
        (item,)
    )
    conn.commit()

# function for adding counts into the db
def add_count(item):
    
    cursor.execute(
        "UPDATE usage SET count = count + 1 WHERE item = ?",
        (item,)
    )
    conn.commit()

def get_counts(items):
    # pobiera liczniki tylko dla podanej listy rzeczy
    placeholders = ",".join("?" * len(items))
    cursor.execute(
        f"SELECT item, count FROM usage WHERE item IN ({placeholders})",
        items
    )
    return cursor.fetchall()


# funtion for fetching counts all counts from the db
def get_all_counts():
    cursor.execute("SELECT item, count FROM usage")
    return cursor.fetchall() 

# resets the counts admin only
def reset_counts():
    cursor.execute("UPDATE usage SET count = 0")
    conn.commit()