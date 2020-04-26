from bs4 import BeautifulSoup as soup
import requests as r


# url -> [{name: str, lang: str, description: Maybe str}]
def scrape_profile(
        url: str) -> [{
            "name": str,
            "lang": str,
            "description": str or None
        }]:
    scrape_url = url + '?tab=repositories'
    projects = []
    source = r.get(scrape_url).text
    page_soup = soup(source, 'lxml')
    repos = page_soup.body.find_next('div', {
        'id': 'user-repositories-list'
    }).ul
    for repo in repos.find_all('li'):
        name = repo.div.div.h3.a.text.strip()
        lang = repo.find_next('span', {'itemprop': 'programmingLanguage'}).text
        description = None
        try:
            description = repo.div.contents[3].p.text.strip()
        except AttributeError:
            pass
        projects.append({
            'name': name,
            'lang': lang,
            'description': description
        })
    return projects
