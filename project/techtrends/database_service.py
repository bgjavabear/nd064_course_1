# Function to get a database connection.
# This function connects to database with the name `database.db`
import sqlite3

connection_count = 0


def get_db_connection():
    global connection_count
    connection_count += 1
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row

    return connection


def find_post_by_id(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


def find_all():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return posts


def create_post(title, content):
    connection = get_db_connection()
    connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                       (title, content))
    connection.commit()
    connection.close()


def get_post_count():
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(*) FROM posts').fetchone()[0]
    return post_count


def is_connection_established():
    try:
        get_db_connection()
        return True
    except sqlite3.Error:
        return False


def is_posts_table_exists():
    connection = get_db_connection()
    table = connection.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = ?',
                               ('posts',)).fetchone()
    return table is not None


def get_connection_count():
    return connection_count
