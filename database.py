import psycopg2
import os

# connects with PostgreSQL by URL fron Railway Variables
# DATABASE_URL is auto set by railway
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
conn.autocommit = True  # auto commits
cursor = conn.cursor()


def setup():
    # if table doesnt exist it creats it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage (
            item  TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0
        )
    """)

    # adds rows with count 1
    for item in [
        # glup
        "glup_emoji", "glup_gif", "glup_sticker",
        # steamhappy
        "steamhappy_emoji", "steamhappy_gif"
    ]:
        cursor.execute(
            "INSERT INTO usage (item, count, total) VALUES (%s, 0, 0) ON CONFLICT (item) DO NOTHING",
            (item,)
        )


def add_count(item):
    # adds one to count of said thing
    cursor.execute(
        "UPDATE usage SET count = count + 1, total = total + 1 WHERE item = %s",
        (item,)
    )


def get_counts(items):
    # gets counts only for said items
    placeholders = ",".join(["%s"] * len(items))
    cursor.execute(
        f"SELECT item, count, total FROM usage WHERE item IN ({placeholders})",
        items
    )
    return cursor.fetchall()

def reset_monthly(items):
    # resets monthly count
    placeholders = ",".join(["%s"] * len(items))
    cursor.execute(
        f"UPDATE usage SET count = 0 WHERE item IN ({placeholders})",
        items
    )

def get_all_counts():
    # gets all counts
    cursor.execute("SELECT item, count, total FROM usage")
    return cursor.fetchall()


def reset_counts():
    # resets counts
    cursor.execute("UPDATE usage SET count = 0")