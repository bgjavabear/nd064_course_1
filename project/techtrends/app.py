import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from database_service import *
import logging, sys

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    posts = find_all()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = find_post_by_id(post_id)
    if post is None:
        app.logger.info('Article with id = "{0}" does not exist.'.format(post_id))
        return render_template('404.html'), 404
    else:
        app.logger.info('Article "{0}" retrieved!'.format(post['title']))
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About page has been requested.')
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            create_post(title, content)
            app.logger.info('Article "{0}" has been created.'.format(title))
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def health_check():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/metrics')
def metrics():
    post_count = get_post_count()
    con_count = get_connection_count()

    response = app.response_class(
        response=json.dumps({"db_connection_count": con_count, "post_count": post_count}),
        status=200,
        mimetype='application/json'
    )

    return response


# start the application on port 3111
if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    app.run(host='0.0.0.0', port='3111')
