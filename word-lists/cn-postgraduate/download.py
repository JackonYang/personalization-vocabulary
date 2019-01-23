import os
import requests

from bs4 import BeautifulSoup


# start_url = 'http://kaoyan.wendu.com/yingyu/fuxi/116298.shtml'
start_url = 'http://kaoyan.koolearn.com/20170209/972676.html'
unit_page_prefix = 'http://kaoyan.koolearn.com/'
unit_page_cnt = 55 * 2


def download(url):
    rsp = requests.get(url, timeout=3)
    return rsp.text


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

    # for url in hrefs:
    #     unit_page = download(url)
    #     unit_soup = BeautifulSoup(unit_page, 'html.parser')
    #     break


if __name__ == '__main__':
    main()
