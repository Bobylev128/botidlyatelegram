import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS votes(
    voter_id INTEGER,
    target TEXT,
    round_n INTEGER,
    group_n INTEGER,
    vote_type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(
    user_id INTEGER,
    amount INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bans(
    user_id INTEGER PRIMARY KEY,
    reason TEXT
)
""")

conn.commit()


def add_user(uid):
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?)", (uid,))
    conn.commit()


def get_all_users():
    return [x[0] for x in cursor.execute("SELECT user_id FROM users")]


def get_voters():
    return [x[0] for x in cursor.execute("SELECT DISTINCT voter_id FROM votes")]


def add_vote(voter, target, r, g, t):
    cursor.execute("INSERT INTO votes VALUES (?,?,?,?,?)", (voter, target, r, g, t))
    conn.commit()


def has_voted_free(voter, r, g):
    return cursor.execute("""
        SELECT 1 FROM votes
        WHERE voter_id=? AND round_n=? AND group_n=? AND vote_type='free'
    """, (voter, r, g)).fetchone()


def count_votes(target, r, g):
    res = {"free": 0, "paid": 0}
    for t, c in cursor.execute("""
        SELECT vote_type, COUNT(*) FROM votes
        WHERE target=? AND round_n=? AND group_n=?
        GROUP BY vote_type
    """, (target, r, g)):
        res[t] = c
    return res


def ban_user(uid, reason):
    cursor.execute("INSERT OR REPLACE INTO bans VALUES (?,?)", (uid, reason))
    conn.commit()


def is_banned(uid):
    return cursor.execute("SELECT reason FROM bans WHERE user_id=?", (uid,)).fetchone()