import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from common import cache_request

BASE_URL = 'https://sos.nebraska.gov/elections/election-officials-contact-information'


def get_key_text(_iter):
  while True:
    elem = next(_iter)
    if isinstance(elem, Tag) and elem.name == 'strong':
      return elem.text.split(':')[0]


def get_val_text(_iter):
  text = ''
  while True:
    elem = next(_iter)
    if isinstance(elem, NavigableString):
      text += elem.strip()
    if isinstance(elem, Tag) and elem.name == 'a':
      text += elem.text.strip()
    if (isinstance(elem, Tag) and elem.name == 'br'):
      return text


def parse_lines(_iter):
  while True:
    try:
      key = get_key_text(_iter)
      val = get_val_text(_iter)

      yield (key, val)
    except StopIteration:
      break


county_re = re.compile(r'(.*) \((\d{1,2})\)')


def parse_county(county):
  _iter = iter(county.children)
  # ignore first two children
  next(_iter)
  next(_iter)
  result = dict(parse_lines(_iter))

  match = county_re.search(result['County'])
  result['County'] = match.group(1)
  result['Id'] = match.group(2)
  assert result['Email Address']
  assert result['Name']
  county = result['County'] + ' County'
  return {
    'locale': county,
    'official': result['Name'],
    'emails': [result['Email Address']],
    'faxes': [result['Fax Number']],
    'phones': [result['Phone Number']],
    'county': county,
    'address': result['Address'],
    'party': result['Party Affiliation'],
  }


def fetch_data():
  text = cache_request(BASE_URL)
  soup = BeautifulSoup(text, 'lxml')

  counties = soup.select('div.field-items>div.field-item div.col-sm-6')
  data = [parse_county(county) for county in counties]
  assert len(data) == 93

  return data


if __name__ == '__main__':
  print(fetch_data())
