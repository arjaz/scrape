from flask import Flask, render_template, request
from scraper import scrape_profile

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST', 'GET'])
def scrape():
    userlink = request.form['userlink']
    # TODO: validate link
    repos = scrape_profile(userlink)
    return render_template('scraped.html', repos=repos)


if __name__ == '__main__':
    app.run(debug=True)
