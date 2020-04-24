from flask import Flask, render_template, request, redirect
from scraper import scrape_profile

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST', 'GET'])
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

    if request.method == 'POST':
        userlink = request.form['userlink']
        if not link(userlink):
            actual_link = f'https://github.com/{userlink}'
        else:
            actual_link = userlink
        repos = scrape_profile(actual_link)
        return render_template('scraped.html', repos=repos)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
