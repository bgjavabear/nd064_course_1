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


def get_connection_count():
    return connection_count
