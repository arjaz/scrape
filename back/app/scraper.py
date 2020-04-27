from bs4 import BeautifulSoup as soup
import requests as r


# url -> Maybe [{name: str, lang: Maybe str, description: Maybe str}]
def scrape_profile(
    url: str
) -> [{
        "name": str,
        "lang": str or None,
        "description": str or None
}] or None:
    scrape_url = url + '?tab=repositories'
    projects = []
    answer = r.get(scrape_url)
    if answer.status_code != 200:
        return None
    source = answer.text
    page_soup = soup(source, 'lxml')
    repos = page_soup.body.find_next('div', {
        'id': 'user-repositories-list'
    }).ul
    for repo in repos.find_all('li'):
        name = repo.div.div.h3.a.text.strip()

        try:
            lang = repo.find_next('span', {
                'itemprop': 'programmingLanguage'
            }).text
        except AttributeError:
            lang = None

        try:
            description = repo.div.contents[3].p.text.strip()
        except AttributeError:
            description = None

        projects.append({
            'name': name,
            'lang': lang,
            'description': description
        })
    return projects
