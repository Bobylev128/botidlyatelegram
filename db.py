import sqlite3

conn = sqlite3.connect("battle.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS battle_participants (
    user_id INTEGER PRIMARY KEY,
    username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER,
    target_username TEXT,
    round_number INTEGER,
    group_number INTEGER,
    vote_type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bans (
    user_id INTEGER PRIMARY KEY,
    reason TEXT
)
""")

conn.commit()


def add_participant_manual(user_id, username):
    cursor.execute("INSERT OR IGNORE INTO battle_participants VALUES (?, ?)", (user_id, username))
    conn.commit()


def get_all_users():
    cursor.execute("SELECT user_id, username FROM battle_participants")
    return cursor.fetchall()


def add_vote(voter_id, target, round_n, group_n, vote_type):
    cursor.execute("""
    INSERT INTO votes (voter_id, target_username, round_number, group_number, vote_type)
    VALUES (?, ?, ?, ?, ?)
    """, (voter_id, target, round_n, group_n, vote_type))
    conn.commit()


def has_voted(voter_id, round_n, group_n):
    cursor.execute("""
    SELECT 1 FROM votes 
    WHERE voter_id=? AND round_number=? AND group_number=? AND vote_type='free'
    """, (voter_id, round_n, group_n))
    return cursor.fetchone() is not None


def count_votes(target, round_n, group_n):
    cursor.execute("""
    SELECT COUNT(*) FROM votes
    WHERE target_username=? AND round_number=? AND group_number=?
    """, (target, round_n, group_n))
    return cursor.fetchone()[0]