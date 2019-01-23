import os
import requests

from bs4 import BeautifulSoup


data_dir = 'raw_html_rsp'

mp3_dir = 'en-mp3'


if not os.path.exists(mp3_dir):
    os.makedirs(mp3_dir)


def download(url, retry=3):
    for i in range(retry):
        try:
            rsp = requests.get(url, timeout=3)
        except Exception as e:
            print('error: %s, %s' % (url, e))
        else:
            return rsp.content
    return ''


def get_files():
    for fn in os.listdir(data_dir):
        with open(os.path.join(data_dir, fn)) as fp:
            yield fn[:-5], ''.join(fp.readlines())


def parse_pron(soup, word):
    unknown = 'unknown'
    node = soup.find('span', class_='pron')
    if not node:
        return unknown
    
    mp3_node = node.find('a')
    
    if not mp3_node:
        return unknown

    return mp3_node['data-src-mp3']


def parse():

    freq_desc = set()
    for word, text in get_files():
        mp3_filename = os.path.join(mp3_dir, '%s.mp3' % word)

        if os.path.exists(mp3_filename):
            continue

        soup = BeautifulSoup(text, 'html.parser')

        mp3_url = parse_pron(soup, word)
        mp3_content = download(mp3_url)

        with open(mp3_filename, 'wb') as fp:
            fp.write(mp3_content)

        print(mp3_filename)

if __name__ == '__main__':
    parse()
