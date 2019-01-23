import json
import time

from fetch import main as fetch_word


initial_list_file = '../../word-lists/gre-3000-v2011/gre-3000-v2011.json'


def initial_list():
    with open(initial_list_file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return data.keys()


def download():
    for word in initial_list():
        if not fetch_word(word):
            time.sleep(1)


if __name__ == '__main__':
    download()
