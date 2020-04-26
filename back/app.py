import os
from flask import Flask, render_template, request, redirect, jsonify
from scraper import scrape_profile
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Repo, User

# TODO: Add caching


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/user/<id_>')
def get_user(id_):
    try:
        user = User.query.filter_by(id=id_).first()
        repos = [repo.serialize() for repo in user.repos]
        print(type(repos))
        print(repos)

        return jsonify(repos)
    except Exception as e:
        return str(e)


@app.route('/api/repository/<id_>')
def get_repo(id_):
    try:
        repo = Repo.query.filter_by(id=id_).first()
        return jsonify(repo.serialize())
    except Exception as e:
        return str(e)


@app.route('/scrape', methods=['POST'])
def scrape():
    # Check link
    def link(url):
        import re
        regex = re.compile(
            r'^(?:http)s?://'  # http:// or https://
            r'(github\.com)|'  # domain
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)
        return re.match(regex, url) is not None

    # Userlink and username extraction
    # TODO: add validation
    userlink = request.form.get('userlink')
    if not link(userlink):
        actual_link = f'https://github.com/{userlink}'
        username = userlink
    else:
        actual_link = userlink
        username = list(filter(lambda x: len(x) > 0,
                               actual_link.split('/')))[-1]

    # Scraping
    repos = scrape_profile(actual_link)

    # Check user
    user = User.query.filter_by(name=username).first()
    if user is None:
        try:
            user = User(name=username, link=f'https://github.com/{username}')
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return str(e)

    # If repo exists, do nothing TODO: update
    # If repo doesn't exist, add it
    for repo in repos:
        try:
            name = repo['name']
            lang = repo['lang']
            description = repo['description'] if repo['description'] else ''

            registered = Repo.query.filter_by(name=name).first()
            if registered is None:
                obj = Repo(name=name,
                           lang=lang,
                           description=description,
                           user_id=user.id)

                db.session.add(obj)
                db.session.commit()
        except Exception as e:
            return str(e)
    return redirect(f'/api/user/{user.id}')


if __name__ == '__main__':
    app.run()
