import requests
import json
import csv
from ftfy import fix_text

from bs4 import BeautifulSoup
import re

record_start_ptn = re.compile('^(?:\d+\s+)?([\-\w]+)\s+(.+$)')


# start_url = 'http://kaoyan.wendu.com/yingyu/fuxi/116298.shtml'
start_url = 'http://kaoyan.koolearn.com/20170209/972676.html'
unit_page_prefix = 'http://kaoyan.koolearn.com/'
unit_page_cnt = 55 * 2

output_basename = 'cn-postgraduate-5500words'


def download(url, retry=3):
    for i in range(retry):
        try:
            rsp = requests.get(url, timeout=3)
        except Exception as e:
            print('error: %s, %s' % (url, e))
        else:
            return rsp.text
    return ''


def convert_json_to_csv(json_filename, csv_filename, csv_headers):
    with open(json_filename, 'r', encoding='utf-8') as f_json:
        with open(csv_filename, 'w', encoding='utf-8') as f_csv:
            csv_writer = csv.writer(f_csv)
            csv_writer.writerow(csv_headers)

            for line in f_json:
                data = json.loads(line)
                csv_record = [data.get(i, '-') for i in csv_headers]
                csv_writer.writerow(csv_record)


def main():
    """
    return skipped: True/False
    """

    list_page = download(start_url)
    soup = BeautifulSoup(list_page, 'html.parser')

    tbody = soup.find('tbody')
    link_nodes = tbody.find_all('a')

    hrefs = list(filter(
        lambda x: x.startswith(unit_page_prefix),
        [a['href'] for a in link_nodes]
    ))

    # print(hrefs)
    assert(len(hrefs) == unit_page_cnt)  # $unit_page_cnt lists

    words = dict()

    for idx, url in enumerate(hrefs):
        unit_page = download(url)
        unit_soup = BeautifulSoup(unit_page, 'html.parser')
        nodes = unit_soup.find('div', class_='mt40').find_all('p')
        texts = list(filter(
            lambda x: record_start_ptn.match(x),
            [fix_text(node.get_text()).strip() for node in nodes]
        ))

        if len(texts) != 50:
            print('warning: ', url, len(texts))
            # print('\n'.join(texts))

        for text in texts:
            m = record_start_ptn.search(text)
            word, explanation = m.groups()
            words[word] = explanation
        print(idx)

    json_filename = '%s.json' % output_basename
    with open(json_filename, 'w', encoding='utf-8') as fp:
        json.dump(words, fp, indent=4)

    csv_filename = '%s.csv' % output_basename
    with open(csv_filename, 'w', encoding='utf-8') as f_csv:
            csv_writer = csv.writer(f_csv)
            csv_writer.writerow(['word', 'explanation'])

            for w, e in words.items():
                csv_writer.writerow([w, e])


if __name__ == '__main__':
    main()
