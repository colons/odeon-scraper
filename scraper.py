from bs4 import BeautifulSoup
import requests


def get_screenings(cinema_id, date=None):
    screenings = []
    resp = requests.get(
        'https://www.odeon.co.uk/cinemas/a/{}/'.format(cinema_id)
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'html5lib')

    for screening_element in soup.select('.film-detail'):
        screening = {}

        name_element, = screening_element.select('.presentation-info h4')
        time_elements = screening_element.select('.times li a')
        screenings.append({
            'title': name_element.get_text(),
            'times': [a['data-start'] for a in time_elements],
        })

    return screenings


if __name__ == '__main__':
    print(get_screenings(104))
