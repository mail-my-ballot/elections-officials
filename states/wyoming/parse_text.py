import json
from common import dir_path

# link to data: https://sos.wyo.gov/Elections/Docs/WYCountyClerks_AbsRequest_VRChange.pdf 

def get_county_dict():
  county = {
    'local': '',
    'official': '',
    'emails': [],
    'faxes': [],
    'phones': [],
    'county': '',
    'party': ''
  }
  return county


def generate_county_dict_list(lines):
  counties = []

  new_county = True
  county = get_county_dict()
  for line in lines:
      line = line.strip(' \n')
      if 'County' in line:
        if not new_county:
          counties.append(county)
          new_county = True
          county = get_county_dict()
        county['locale'] = line[:-len(' Clerk')]
        county['county'] = line[:-len(' Clerk')]
        new_county = False
      elif '@' in line:
        if line.startswith('Email: '):
          line =  line[len('Email: '):]
        county['emails'].append(line)
      elif 'Ph.' in line:
        county['phones'].append(line.strip('Ph. ').replace('.', '-'))
      elif 'Fax' in line:
        county['faxes'].append(line.strip('Fax ').replace('.', '-'))
      else:
        if len(line) > 3:
          if 'address' not in county:
            county['address'] = ''
          county['address'] += (line + ' ')

  return counties


def main():
  with open(dir_path(__file__) + '/results/wyoming_contact_organized.txt', 'r') as fh:
    lines = fh.readlines()
    counties = generate_county_dict_list(lines)

  with open(dir_path(__file__) + '/results/records.noemail.json', 'w') as fh:
    json.dump(counties, fh)

  with open('public/wyoming.json', 'w') as f:
    json.dump(counties, f)


if __name__ == '__main__':
  main()
