# -*- coding=utf-8 -*-

from collections import OrderedDict
import os
from os.path import abspath, join
import re
import time
from tqdm import tqdm
import urllib.request

def store_html_from_source(args):
  try:
      fi = open(abspath(args.url_list))
      print('reading a file: ', abspath(args.url_list))
      urls = fi.readlines()
  except OSError as err:
      print('FileNotFound:')
      print(err)
  finally:
    fi.close()

  with tqdm(urls, ncols=100) as pbar:
    for i, url in enumerate(pbar):
      # in V9.0.0 CSQZ message is added.
      filename = re.search(r'csq_[bcehijmnopqrtuvwxyz012359]{1}',url)
      pbar.set_postfix(OrderedDict(MessageType=filename.group()))
      try:
        src = http_request(url)
        fo = open(join(abspath(args.output_path), filename.group() + '.html'), 'w')
        fo.write(str(src))
      except OSError as err:
        print(err)
      finally:
        fo.close()

def http_request(url):
    try:
        # Intentionally put a delay(1 second) to reduce the load on the serve
        time.sleep(1.0)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
          return res.read()
    except urllib.error.HTTPError as err:
        print(err.code)
    except urllib.error.URLError as err:
        print(err.reason)