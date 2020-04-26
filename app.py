import os
from flask import Flask, render_template, request, redirect, jsonify
from scraper import scrape_profile
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Repo

# TODO: add api with jsonify


@app.route('/')
def index():
    return render_template('index.html')


# TODO: add user specification
@app.route('/repositories')
def repositories():
    return "TODO"
    pass


@app.route('/api/repository/<id_>')
def get_repo(id_):
    try:
        repo = Repo.query.filter_by(id=id_).first()
        return jsonify(repo.serialize())
    except Exception as e:
        return str(e)


@app.route('/scrape', methods=['POST'])
def scrape():
    def link(url):
        import re
        regex = re.compile(
            r'^(?:http)s?://'  # http:// or https://
            r'(github\.com)|'  #domain...
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)
        return re.match(regex, url) is not None

    userlink = request.form['userlink']
    if not link(userlink):
        # TODO: Add name validation
        actual_link = f'https://github.com/{userlink}'
    else:
        actual_link = userlink
    repos = scrape_profile(actual_link)
    # TODO redirect to user profile with all his repositories
    for repo in repos:
        try:
            name = repo['name']
            lang = repo['lang']
            description = repo['description'] if repo['description'] else ''
            obj = Repo(name=name, lang=lang, description=description)

            db.session.add(obj)
            db.session.commit()
            return redirect(f'/api/repository/{obj.id}')
        except Exception as e:
            return str(e)
    return redirect('/')


if __name__ == '__main__':
    app.run()
