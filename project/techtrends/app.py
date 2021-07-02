import logging
import sys

from flask import Flask, json, render_template, request, url_for, redirect, flash

from database_service import *

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
    is_db_connection_established = is_connection_established()
    is_table_exists = is_posts_table_exists()
    is_app_responsive = is_db_connection_established and is_table_exists

    if is_app_responsive:
        response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy"}),
            status=500,
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
