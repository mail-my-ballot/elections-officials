import os
import requests
import argparse
import time
import hashlib

from ediblepickle import checkpoint


def dir_path(_file_):
  return os.path.dirname(os.path.realpath(_file_))

sha256 = lambda x: hashlib.sha256(x.encode('utf8')).hexdigest()

def key_namer(args, kwargs):
  wait_free = { k: v for k, v in kwargs.items() if k != 'wait' }
  return sha256(str(args) + str(wait_free)) + '.pkl'

work_dir = dir_path(__file__) + '/../../cache/'

@checkpoint(key=key_namer, work_dir=work_dir)
def cache_request(url, method='GET', data={}, wait=None):
  if wait is not None:
    time.sleep(wait)
  if data:
    response = requests.request(method, url, data=data)
  else:
    response = requests.request(method, url)
  return response.text

def to_list(x):
  if x:
    return [x]
  else:
    return []

def arg_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("--crawl", action="store_true")
  return parser.parse_args()

def decode_email(e):
  '''
  Decrypts a CloudFlare-obfuscuated email address.
  https://stackoverflow.com/questions/36911296/scraping-of-protected-email
  '''
  de = ""
  k = int(e[:2], 16)

  for i in range(2, len(e)-1, 2):
    de += chr(int(e[i:i+2], 16)^k)

  return de
