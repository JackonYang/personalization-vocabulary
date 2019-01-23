import os
from bs4 import BeautifulSoup


data_dir = 'raw_html_rsp'


if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def get_files():
    for fn in os.listdir(data_dir):
        with open(os.path.join(data_dir, fn)) as fp:
            yield fn[:-5], ''.join(fp.readlines())


def parse_freq(soup, word):
    unknown = 'unknown'
    trends_node = soup.find('div', attrs={'data-type-block': 'Trends'})
    if not trends_node:
        return unknown
    
    info_node = trends_node.find('p')
    
    if not info_node:
        return unknown

    text = info_node.get_text()

    dot_idx = text.find('.')
    return text[:dot_idx].strip().lower()


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
        soup = BeautifulSoup(text, 'html.parser')

        # print('%s: %s' % (word, parse_freq(soup, word)))
        print(word, parse_pron(soup, word))
    
    print('\n'.join(freq_desc))


if __name__ == '__main__':
    parse()